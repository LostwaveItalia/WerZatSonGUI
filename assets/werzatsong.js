/*
 * Originally from https://github.com/Nel80s/WerZatSong by Nel, with
 * contributions from Numerophobe, AzureBlast and Mystic65.
 * Reworked by some random account and EierkuchenHD to work with WerZatSonGUI, additional changes were also implemented.
 */

const dotenv = require('dotenv')
const { execFile, spawn } = require('node:child_process')
const crypto = require('node:crypto')
const { copyFileSync, createReadStream, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, unlinkSync, writeFileSync } = require('node:fs')
const { availableParallelism } = require('node:os')
const { basename, extname, join } = require('node:path')
const readline = require('node:readline')
const { promisify } = require('node:util')
const { hideBin } = require('yargs/helpers')
const yargs = require('yargs/yargs')
const { searchWithAudiotag } = require('./scripts/audiotag')
const consts = require('./utils/consts')
const { generateUnique, sleep, trimExtension } = require('./utils/helpers')
const { t } = require('./utils/i18n')
const { empty, exit, info, success, warning } = require('./utils/messages')
const { validateAudiotag, validateDuration, validateExtension, validateMusicbrainz, validateWebhook } = require('./utils/validators')
const postWebhook = require('./utils/webhook')

require('node:events').setMaxListeners(100) // increase listeners limit

const AUDFPRINT_VERY_STRONG_ALIGNED = 70   // aligned hashes, high enough to trust on their own
const AUDFPRINT_STRONG_ALIGNED = 40        // aligned hashes...
const AUDFPRINT_STRONG_CONSISTENCY = 2     // ...at this aligned/raw percentage
const AUDFPRINT_PROBABLE_ALIGNED = 25      // aligned hashes...
const AUDFPRINT_PROBABLE_CONSISTENCY = 7   // ...at this aligned/raw percentage
const AUDFPRINT_REVIEW_ALIGNED = 10        // below webhook threshold, but there could still be a match there (log-only)

const DEFAULT_QUERY_SHIFTS = 4             // query-side audfprint --shifts
const DEFAULT_MERGE_SHARD_FILES = 64       // source pklz files merged per output shard in --merge mode
const MAX_FILES_PER_SEARCH = 30            // amount
const MAX_PREP_CONCURRENCY = 8             // upper bound for parallel ffmpeg/precompute workers
const MUSICBRAINZ_MIN_SCORE = 60           // percentage
const PROGRAM_VERSION = 'v2.1.0'
const RESULTS_FOLDER = join(consts.LOGS_FOLDER, generateUnique())
const SHAZAM_SLEEP = 1.5                   // seconds
const WEBHOOK_SLEEP = 2                    // seconds between Discord posts

const CACHE_FOLDER = join(consts.INPUT_FOLDER, '..', 'cache', 'afpt')

const Mode = {
    AUDFPRINT: 'audfprint',
    AUDIOTAG: 'audiotag',
    MUSICBRAINZ: 'musicbrainz',
    SHAZAM: 'shazam'
}

const execFileP = promisify(execFile)
const { argv } = yargs(hideBin(process.argv))
// Program version
.version(PROGRAM_VERSION)
// Search modes
.option(Mode.AUDFPRINT, { type: 'boolean', description: 'Enable Audfprint-based matching' })
.option(Mode.AUDIOTAG, { type: 'boolean', description: 'Enable search using the Audiotag API' })
.option(Mode.MUSICBRAINZ, { type: 'boolean', description: 'Enable search using MusicBrainz (AcoustID API)' })
.option(Mode.SHAZAM, { type: 'boolean', description: 'Enable search using Shazam API' })
// Global options
.option('trim', { type: 'number', description: 'Trim MP3 files to the specified length (in seconds) before processing' })
// MusicBrainz options
.option('duration', { type: 'string', description: 'Set the allowed duration range for MusicBrainz searches (format: "min:max")' })
.option('extension', { type: 'number', description: 'Extend MP3 files by the specified number of seconds before MusicBrainz analysis' })
// Audfprint options
.option('folder', { type: 'string', description: 'Specify the subfolder containing PKLZ files to be used in Audfprint mode' })
.option('threads', { type: 'number', description: 'Set the number of threads to use for Audfprint processing' })
.option('shifts', { type: 'number', description: `Query-side audfprint --shifts (1-8). Higher is more robust but linearly slower; default ${DEFAULT_QUERY_SHIFTS}` })
// Database maintenance
.option('merge', { type: 'string', description: 'Merge the PKLZ files in "database/<folder>" into a few large shards (major speedup), then exit. Pass "" for the database root' })
.option('shard-files', { type: 'number', description: `In --merge mode, how many source PKLZ files go into each merged shard (default ${DEFAULT_MERGE_SHARD_FILES})` })

/* ---------------------------------------------------------------------------
 * Small generic helpers
 * ------------------------------------------------------------------------ */

function splitCommand(command){
    const trimmed = (command || '').trim()
    if(trimmed === '')
        return { exe: trimmed, preArgs: [] }
    if(existsSync(trimmed))
        return { exe: trimmed, preArgs: [] }
    const parts = trimmed.split(/\s+/)
    return { exe: parts[0], preArgs: parts.slice(1) }
}

function runTool(command, args, options = {}){
    const { exe, preArgs } = splitCommand(command)
    return execFileP(exe, [...preArgs, ...args], {
        maxBuffer: 64 * 1024 * 1024,
        windowsHide: true,
        ...options
    })
}

async function runPool(items, limit, worker){
    const results = new Array(items.length)
    let next = 0
    const lanes = Array.from({ length: Math.max(1, Math.min(limit, items.length)) }, async () => {
        while(next < items.length){
            const index = next++
            results[index] = await worker(items[index], index)
        }
    })
    await Promise.all(lanes)
    return results
}

function hashFile(path){
    return new Promise((resolve, reject) => {
        const hash = crypto.createHash('sha1')
        const stream = createReadStream(path)
        stream.on('error', reject)
        stream.on('data', chunk => hash.update(chunk))
        stream.on('end', () => resolve(hash.digest('hex')))
    })
}

function findFileRecursively(dir, filename){
    let entries
    try { entries = readdirSync(dir, { withFileTypes: true }) }
    catch { return null }
    for(const entry of entries){
        const fullPath = join(dir, entry.name)
        if(entry.isDirectory()){
            const found = findFileRecursively(fullPath, filename)
            if(found)
                return found
        }
        else if(entry.isFile() && entry.name === filename)
            return fullPath
    }
    return null
}

function parseNumericField(value){
    if(typeof value === 'number')
        return value
    const parsed = parseFloat(String(value ?? '').replace(/[^0-9.eE+-]/g, ''))
    return isNaN(parsed) ? 0 : parsed
}

function formatSeconds(ms){
    const totalSeconds = Math.round(ms / 1000)
    const minutes = Math.floor(totalSeconds / 60)
    const seconds = totalSeconds % 60
    return minutes > 0 ? `${minutes}m ${seconds}s` : `${seconds}s`
}

/* ---------------------------------------------------------------------------
 * Setup / input loading
 * ------------------------------------------------------------------------ */

function setupFolders(){
    const foldersToClean = [
        consts.PRECOMPUTED_FOLDER,
        consts.PROCESSED_FOLDER,
        consts.TEMP_FOLDER
    ]
    for(const folder of foldersToClean){
        if(existsSync(folder))
            rmSync(folder, { recursive: true })
        mkdirSync(folder)
    }
    const foldersToCreate = [
        ...foldersToClean,
        consts.DATABASE_FOLDER,
        consts.INPUT_FOLDER,
        consts.LOGS_FOLDER
    ]
    for(const folder of foldersToCreate){
        if(!existsSync(folder))
            mkdirSync(folder)
    }
    if(!existsSync(CACHE_FOLDER))
        mkdirSync(CACHE_FOLDER, { recursive: true })
}

function fetchEnvironment(){
    if(!existsSync(consts.ENV_FILE))
        copyFileSync(consts.EXAMPLE_ENV_FILE, consts.ENV_FILE)
    const { parsed } = dotenv.config({ path: consts.ENV_FILE })
    return parsed
}

function parseModes(){
    const modes = []
    if(argv.audfprint)
        modes.push(Mode.AUDFPRINT)
    if(argv.audiotag)
        modes.push(Mode.AUDIOTAG)
    if(argv.musicbrainz)
        modes.push(Mode.MUSICBRAINZ)
    if(argv.shazam)
        modes.push(Mode.SHAZAM)
    if(modes.length === 0)
        exit(t('choose_at_least_one_mode', { modes: Object.values(Mode).map(value => `--${value}`).join(', ') }))
    return modes
}

function loadSamples(modes){
    const inputEntries = readdirSync(consts.INPUT_FOLDER)
    const audioFiles = inputEntries.filter(filename => filename.toLowerCase().endsWith('.mp3'))
    const precomputedFiles = inputEntries.filter(filename => filename.toLowerCase().endsWith('.afpt'))
    if(modes.some(mode => mode !== Mode.AUDFPRINT) && audioFiles.length === 0)
        exit(t('need_mp3_file_for_modes', { audiotag: Mode.AUDIOTAG, musicbrainz: Mode.MUSICBRAINZ, shazam: Mode.SHAZAM }))
    if(audioFiles.length > MAX_FILES_PER_SEARCH)
        exit(t('too_many_mp3_files', { limit: MAX_FILES_PER_SEARCH, count: audioFiles.length }))
    if(modes.includes(Mode.AUDFPRINT) && audioFiles.length === 0 && precomputedFiles.length === 0)
        exit(t('audfprint_need_mp3_or_afpt', { audfprint: Mode.AUDFPRINT }))
    const mp3Basenames = audioFiles.map(file => trimExtension(file))
    const afptBasenames = precomputedFiles.map(file => trimExtension(file))
    const collisions = mp3Basenames.filter(base => afptBasenames.includes(base))
    if(collisions.length > 0){
        const collisionFiles = collisions.map(base => `- ${base}.mp3 / ${base}.afpt\n`).join('')
        exit(t('duplicate_filename_collisions', { files: collisionFiles }))
    }
    const totalFiles = audioFiles.length + precomputedFiles.length
    if(modes.includes(Mode.AUDFPRINT) && totalFiles > MAX_FILES_PER_SEARCH)
        exit(t('too_many_files_audfprint', { audfprint: Mode.AUDFPRINT, limit: MAX_FILES_PER_SEARCH, count: totalFiles }))
    return { audioFiles, precomputedFiles }
}

/* ---------------------------------------------------------------------------
 * Query preparation: trim + precompute, run in parallel with caching
 * ------------------------------------------------------------------------ */

async function trimFile(ffmpegCommand, filename, seconds){
    try {
        const originalPath = join(consts.INPUT_FOLDER, filename)
        const trimmedPath = join(consts.PROCESSED_FOLDER, filename)
        await runTool(ffmpegCommand, ['-i', originalPath, '-y', '-t', String(seconds), trimmedPath])
        return true
    }
    catch(error){
        warning(t('trim_failed', { file: filename, error: error.message }))
        return false
    }
}

async function precomputeFile(pythonCommand, filename, shifts){
    const sourcePath = join(consts.PROCESSED_FOLDER, filename)
    const afptName = `${trimExtension(filename)}.afpt`
    const targetPath = join(consts.PRECOMPUTED_FOLDER, afptName)
    try {
        const { stdout } = await runTool(pythonCommand, [
            consts.AUDFPRINT_PROGRAM,
            'precompute',
            '--precompdir', consts.PRECOMPUTED_FOLDER,
            '--shifts', String(shifts),
            sourcePath
        ])
        if(stdout.includes('Zero length analysis')){
            warning(t('precompute_too_short', { file: filename, audfprint: Mode.AUDFPRINT }))
            return null
        }
        if(existsSync(targetPath))
            return targetPath
        const produced = findFileRecursively(consts.PRECOMPUTED_FOLDER, afptName)
        if(produced){
            if(produced !== targetPath)
                copyFileSync(produced, targetPath)
            return targetPath
        }
        warning(t('precompute_missing_output', { file: filename, afpt: afptName }))
        return null
    }
    catch(error){
        warning(t('precompute_failed', { file: filename, error: error.message }))
        return null
    }
}

async function generateFiles(env, trimSeconds, shifts, modes, audioFiles, precomputedFiles){
    const filesToProcess = { afpts: [], mp3s: [] }
    const wantAfpt = modes.includes(Mode.AUDFPRINT)
    const needMp3 = modes.some(mode => mode !== Mode.AUDFPRINT)
    const trimming = !isNaN(Number(trimSeconds)) && trimSeconds > 0
    let skipped = 0
    let cacheHits = 0

    if(audioFiles?.length > 0){
        const concurrency = Math.max(1, Math.min(availableParallelism(), MAX_PREP_CONCURRENCY, audioFiles.length))
        if(audioFiles.length > 1)
            info(t('preparing_input_files', { count: audioFiles.length, concurrency }))

        const prepared = await runPool(audioFiles, concurrency, async audioFile => {
            const result = { mp3: null, afpt: null, ok: true }
            const originalPath = join(consts.INPUT_FOLDER, audioFile)
            const processedPath = join(consts.PROCESSED_FOLDER, audioFile)

            let cachedPath = null
            let cacheHit = false
            if(wantAfpt){
                try {
                    const contentHash = await hashFile(originalPath)
                    cachedPath = join(CACHE_FOLDER, `${contentHash}-t${trimming ? trimSeconds : 0}-s${shifts}.afpt`)
                    cacheHit = existsSync(cachedPath)
                }
                catch { /* unreadable file - treat as a cache miss, real errors surface below */ }
            }

            const needProcessed = needMp3 || (wantAfpt && !cacheHit)
            if(needProcessed){
                if(trimming){
                    if(!await trimFile(env.FFMPEG_COMMAND, audioFile, trimSeconds)){
                        result.ok = false
                        return result
                    }
                }
                else {
                    try { copyFileSync(originalPath, processedPath) }
                    catch(error){
                        warning(t('copy_failed_skip', { file: audioFile, error: error.message }))
                        result.ok = false
                        return result
                    }
                }
                if(needMp3)
                    result.mp3 = processedPath
            }

            if(wantAfpt){
                const targetAfpt = join(consts.PRECOMPUTED_FOLDER, `${trimExtension(audioFile)}.afpt`)
                if(cacheHit){
                    try {
                        copyFileSync(cachedPath, targetAfpt)
                        result.afpt = targetAfpt
                        cacheHits += 1
                        return result
                    }
                    catch { /* corrupt cache entry, fall through and recompute instead */ }
                }
                const produced = await precomputeFile(env.PYTHON_COMMAND, audioFile, shifts)
                if(produced){
                    result.afpt = produced
                    if(cachedPath){
                        try { copyFileSync(produced, cachedPath) }
                        catch { /* just failing to write the cache, not worth aborting over */ }
                    }
                }
            }
            return result
        })

        for(const item of prepared){
            if(!item.ok){
                skipped += 1
                continue
            }
            if(item.mp3)
                filesToProcess.mp3s.push(item.mp3)
            if(item.afpt)
                filesToProcess.afpts.push(item.afpt)
        }
        if(cacheHits > 0)
            success(t('cache_reused', { hits: cacheHits, total: audioFiles.length }))
        if(skipped > 0)
            warning(t('skipped_files_due_to_errors', { count: skipped }))
        if(skipped === audioFiles.length && audioFiles.length > 0 && precomputedFiles?.length === 0)
            exit(t('all_files_failed_to_prepare'))
    }

    if(wantAfpt && precomputedFiles?.length > 0){
        for(const precomputedFile of precomputedFiles){
            copyFileSync(join(consts.INPUT_FOLDER, precomputedFile), join(consts.PRECOMPUTED_FOLDER, precomputedFile))
            filesToProcess.afpts.push(join(consts.PRECOMPUTED_FOLDER, precomputedFile))
        }
    }
    return filesToProcess
}

/* ---------------------------------------------------------------------------
 * Results logging
 * ------------------------------------------------------------------------ */

function createResultsLog(basename, mode, content){
    if(!existsSync(RESULTS_FOLDER))
        mkdirSync(RESULTS_FOLDER)
    const resultsFile = join(RESULTS_FOLDER, `${basename}.${mode}.txt`)
    writeFileSync(resultsFile, content)
    return resultsFile
}

function fetchFingerprints(targetFolder){
    let pklzFiles = []
    const fetchFilesRecursively = dir => {
        const files = readdirSync(dir, { withFileTypes: true })
        for(const file of files){
            const fullPath = join(dir, file.name)
            if(file.isDirectory())
                fetchFilesRecursively(fullPath)
            else if(file.isFile() && file.name.endsWith('.pklz'))
                pklzFiles.push(fullPath)
        }
    }
    fetchFilesRecursively(targetFolder)
    return pklzFiles
}

function setupAudfprint(folder){
    const baseFolder = join(consts.DATABASE_FOLDER, folder ? folder.trim() : '')
    if(!existsSync(baseFolder))
        exit(t('folder_not_found_in_database', { folder }))
    const pklzFiles = fetchFingerprints(baseFolder)
    if(pklzFiles.length === 0)
        exit(t('no_pklz_files_found', { folder: baseFolder }))
    writeFileSync(consts.PKLZS_FILE, pklzFiles.join('\n'))
    return pklzFiles.length
}

/* ---------------------------------------------------------------------------
 * audfprint worker invocation
 * ------------------------------------------------------------------------ */

function audfprint(env, threads){
    return new Promise((resolve, reject) => {
        const { exe, preArgs } = splitCommand(env.NODE_COMMAND)
        const audfprintProcess = spawn(exe, [...preArgs, consts.AUDFPRINT_SCRIPT, '--threads', String(threads)], { windowsHide: true })
        const stderrTail = []

        readline.createInterface({ input: audfprintProcess.stdout }).on('line', line => {
            if(line.trim() !== '')
                info(line.trim())
        })
        readline.createInterface({ input: audfprintProcess.stderr }).on('line', line => {
            const text = line.trim()
            if(text === '')
                return
            stderrTail.push(text)
            if(stderrTail.length > 40)
                stderrTail.shift()
            warning(t('worker_stderr', { text }))
        })
        audfprintProcess.on('error', error => {
            exit(t('audfprint_launch_failed', { audfprint: Mode.AUDFPRINT, error: error.message }))
        })
        audfprintProcess.on('close', code => {
            if(code === 0)
                return resolve()
            const tail = stderrTail.join('\n')
            if(tail.includes('MemoryError'))
                exit(t('out_of_memory'))
            warning(t('audfprint_exit_error', { audfprint: Mode.AUDFPRINT, code }))
            if(tail !== '')
                warning(t('last_worker_stderr', { tail }))
            reject(new Error(`audfprint worker exited with code ${code}`))
        })
    })
}

/* ---------------------------------------------------------------------------
 * audfprint results: scoring, log formatting, run summary
 * ------------------------------------------------------------------------ */

function classifyMatch(aligned, consistencyPct){
    if(aligned >= AUDFPRINT_VERY_STRONG_ALIGNED)
        return 'very strong'
    if(aligned >= AUDFPRINT_STRONG_ALIGNED && consistencyPct >= AUDFPRINT_STRONG_CONSISTENCY)
        return 'strong'
    if(aligned >= AUDFPRINT_PROBABLE_ALIGNED && consistencyPct >= AUDFPRINT_PROBABLE_CONSISTENCY)
        return 'probable'
    if(aligned >= AUDFPRINT_REVIEW_ALIGNED && consistencyPct >= AUDFPRINT_STRONG_CONSISTENCY)
        return 'borderline' // def worth a manual look, but not in webhook message
    return null
}

function extractPklzName(resultKey){
    const matches = String(resultKey).match(/[^:\\\/|]+\.pklz/gi)
    return matches ? matches[matches.length - 1] : 'unknown.pklz'
}

const LOG_LEGEND = [
    'LEGEND',
    '  Each entry is two lines:',
    '    [LABEL] <aligned> aligned / <raw> raw (<cons>%) | x<hits> | #<rank> | <source pklz> | offset <t>s',
    '    <matched file name> (<matched file path>)',
    '',
    '  aligned : time-consistent matching hashes - the primary evidence.',
    '            audfprint\'s docs: more than 5-6 aligned hashes usually means a true match.',
    '  raw     : all hashes the query and reference have in common, before time filtering.',
    '  cons%   : aligned / raw. Random chance stays under ~1%, so even a few percent is meaningful.',
    '  hits    : how many alignment hits the worker reported for this pair.',
    '  rank    : candidate position in audfprint\'s raw pre-ranking (diagnostic, not confidence).',
    '  offset  : query start relative to the reference, in seconds (negative = query starts earlier).',
    '  LABEL   : VERY STRONG / STRONG / PROBABLE are webhook-worthy; BORDERLINE = review manually;',
    '            NO MATCH = below every threshold, listed for completeness.',
    '',
    ''
].join('\n')

function formatMatchEntry(match){
    const label = (match.confidence || 'no match').toUpperCase()
    const header = `[${label}] ${match.aligned_hashes} aligned / ${match.raw_common_hashes} raw `
        + `(${match.consistency_pct.toFixed(2)}%) | x${match.hits} | #${match.rank} | `
        + `${match.source_pklz} | offset ${match.offset_s}s`
    return `${header}\n${match.matched_basename} (${match.matched_file})\n`
}

function buildMatchReport(matches){
    return matches.map(formatMatchEntry).join('\n')
}

async function createAudfprintLogs(env){
    if(!existsSync(consts.RESULTS_FILE)){
        warning(t('no_audfprint_results_file', { audfprint: Mode.AUDFPRINT }))
        return []
    }
    let results
    try {
        results = JSON.parse(readFileSync(consts.RESULTS_FILE, 'utf-8'))
    }
    catch(error){
        warning(t('could_not_parse_results', { audfprint: Mode.AUDFPRINT, error: error.message }))
        return []
    }

    const matchesByInput = {}
    for(const [resultKey, match] of Object.entries(results)){
        const inputBasename = trimExtension(basename(match.input_file))
        const aligned = Number(match.common_hashes) || 0
        const rawCommon = Number(match.total_hashes) || 0
        const consistencyPct = rawCommon > 0 ? (aligned / rawCommon) * 100 : 0
        if(!matchesByInput[inputBasename])
            matchesByInput[inputBasename] = []
        matchesByInput[inputBasename].push({
            query: inputBasename,
            matched_file: match.matched_file,
            matched_basename: basename(match.matched_file),
            aligned_hashes: aligned,
            raw_common_hashes: rawCommon,
            consistency_pct: consistencyPct,
            hits: match.counter,
            rank: parseNumericField(match.rank_position),
            offset_s: parseNumericField(match.match_time),
            source_pklz: extractPklzName(resultKey),
            confidence: classifyMatch(aligned, consistencyPct)
        })
    }

    const summary = []
    for(const [inputBasename, matches] of Object.entries(matchesByInput)){
        matches.sort((a, b) => b.aligned_hashes - a.aligned_hashes)

        createResultsLog(inputBasename, Mode.AUDFPRINT, `${LOG_LEGEND}${buildMatchReport(matches)}`)

        summary.push({ query: inputBasename, best: matches[0] || null })

        const webhookMatches = matches.filter(match =>
            match.confidence !== null && match.confidence !== 'borderline')
        if(webhookMatches.length > 0){
            const tempFile = join(consts.TEMP_FOLDER, `${inputBasename}.webhook.txt`)
            writeFileSync(tempFile, `${LOG_LEGEND}${buildMatchReport(webhookMatches)}`, 'utf-8')
            // Not necessarily really an .mp3: the query here could be a precomputed .afpt
            // submitted directly with no real audio companion in this run at all, so the
            // basename alone (no fabricated extension) is the only thing known for sure.
            await sleep(WEBHOOK_SLEEP)
            try {
                await postWebhook(env.WEBHOOK_URL, `[${Mode.AUDFPRINT}]: ${inputBasename}`, tempFile)
                success(t('match_found_webhook_sent', { file: inputBasename, mode: Mode.AUDFPRINT }))
            }
            catch(error){
                warning(t('match_found_webhook_failed', { file: inputBasename, error: error.message }))
            }
            unlinkSync(tempFile)
        }
    }
    return summary
}

function printAudfprintSummary(summary){
    if(summary.length === 0)
        return
    info(t('audfprint_summary_header'))
    for(const { query, best } of summary){
        if(!best){
            empty(t('no_candidates_returned', { query }))
            continue
        }
        const description = `${best.aligned_hashes} aligned (${best.consistency_pct.toFixed(2)}% consistent) -> ${best.matched_basename} [${best.source_pklz}]`
        if(best.confidence && best.confidence !== 'borderline')
            success(t('confident_match', { query, confidence: best.confidence.toUpperCase(), description }))
        else if(best.confidence === 'borderline')
            warning(t('borderline_match', { query, description }))
        else
            empty(t('no_confident_match', { query, description }))
    }
}

/* ---------------------------------------------------------------------------
 * Database consolidation (--merge)
 * ------------------------------------------------------------------------ */

function runMergeShard(env, shardPath, listFile){
    return new Promise(resolve => {
        const { exe, preArgs } = splitCommand(env.PYTHON_COMMAND)
        const child = spawn(exe, [
            ...preArgs,
            consts.AUDFPRINT_PROGRAM,
            'newmerge',
            '--dbase', shardPath,
            '--list',
            listFile
        ], { windowsHide: true })
        const stderrTail = []
        readline.createInterface({ input: child.stdout }).on('line', line => {
            if(line.trim() !== '')
                info(`  ${line.trim()}`)
        })
        readline.createInterface({ input: child.stderr }).on('line', line => {
            if(line.trim() === '')
                return
            stderrTail.push(line.trim())
            if(stderrTail.length > 20)
                stderrTail.shift()
        })
        child.on('error', error => {
            warning(t('shard_launch_failed', { error: error.message }))
            resolve(false)
        })
        child.on('close', code => {
            if(code === 0)
                return resolve(true)
            warning(t('shard_merge_failed', { code }))
            if(stderrTail.length > 0)
                warning(t('shard_last_output', { output: stderrTail.join('\n') }))
            resolve(false)
        })
    })
}

async function mergeDatabase(env, folderArg, shardFilesArg){
    const folder = (folderArg || '').trim()
    const baseFolder = join(consts.DATABASE_FOLDER, folder)
    if(!existsSync(baseFolder))
        exit(t('folder_not_found_in_database', { folder }))
    const pklzFiles = fetchFingerprints(baseFolder).filter(path => !path.includes('__merged'))
    if(pklzFiles.length === 0)
        exit(t('no_pklz_files_to_merge', { folder: baseFolder }))
    const perShard = (!isNaN(shardFilesArg) && shardFilesArg > 0) ? Math.floor(shardFilesArg) : DEFAULT_MERGE_SHARD_FILES
    const mergedName = `${folder || 'all'}__merged`
    const outDir = join(consts.DATABASE_FOLDER, mergedName)
    if(!existsSync(outDir))
        mkdirSync(outDir, { recursive: true })

    info(t('merging_pklz_info', { count: pklzFiles.length, perShard }))
    info(t('merge_why_it_helps'))
    warning(t('merge_bucket_warning'))

    const startedAt = Date.now()
    let merged = 0
    let failed = 0
    let shardIndex = 0
    for(let start = 0; start < pklzFiles.length; start += perShard){
        shardIndex += 1
        const shard = pklzFiles.slice(start, start + perShard)
        const shardName = `merged-${String(shardIndex).padStart(3, '0')}.pklz`
        const shardPath = join(outDir, shardName)
        const listFile = join(consts.TEMP_FOLDER, `merge-shard-${shardIndex}.txt`)
        writeFileSync(listFile, shard.join('\n'))
        info(t('merging_shard_progress', { index: shardIndex, total: Math.ceil(pklzFiles.length / perShard), count: shard.length, name: shardName }))
        const ok = await runMergeShard(env, shardPath, listFile)
        ok ? merged += 1 : failed += 1
        try { unlinkSync(listFile) } catch { /* best effort cleanup */ }
    }

    const failedSuffix = failed > 0 ? t('merge_failed_suffix', { count: failed }) : ''
    info(t('merge_finished', { duration: formatSeconds(Date.now() - startedAt), merged, failedSuffix, name: mergedName }))
    if(merged > 0)
        success(t('merge_usage_hint', { audfprint: Mode.AUDFPRINT, name: mergedName }))
    if(failed > 0)
        warning(t('merge_failed_shards_skipped'))
}

/* ---------------------------------------------------------------------------
 * Other search modes
 * ------------------------------------------------------------------------ */

async function musicbrainz(env, file, extension, duration){
    const fileBasename = basename(file)
    try {
        await runTool(env.NODE_COMMAND, [consts.FPCALC_SCRIPT, '--file', file, '--extension', String(extension)])
        const { stdout } = await runTool(env.NODE_COMMAND, [consts.MUSICBRAINZ_SCRIPT, '--file', basename(file), '--duration', duration])
        const outputLogs = stdout.split('\n').filter(line => line.trim() !== '').map(line => JSON.parse(line))
        const results = []
        for(const outputLog of outputLogs){
            if(outputLog.error)
                exit(t('invalid_acoustid_key', { data: outputLog.data }))
            for(const result of outputLog.data){
                if(parseFloat(result.score) >= MUSICBRAINZ_MIN_SCORE)
                    results.push(`[${result.score}% | EXT-${result.extension} | DUR-${result.duration}]: ${consts.ACOUSTID_TRACK_ENDPOINT}/${result.trackId}`)
            }
        }
        if(results.length > 0){
            const resultsFile = createResultsLog(trimExtension(fileBasename), Mode.MUSICBRAINZ, `${results.join('\n')}\n`)
            try {
                await postWebhook(env.WEBHOOK_URL, `[${Mode.MUSICBRAINZ}]: ${fileBasename}`, resultsFile)
                success(t('match_found_webhook_sent', { file: fileBasename, mode: Mode.MUSICBRAINZ }))
            }
            catch(error){
                warning(t('match_found_webhook_failed', { file: fileBasename, error: error.message }))
            }
        }
        else
            empty(t('no_match_found', { file: fileBasename, mode: Mode.MUSICBRAINZ }))
    }
    catch(error){
        warning(t('search_failed', { mode: Mode.MUSICBRAINZ, file: fileBasename, error: error.message }))
    }
}

async function audiotag(env, file){
    const fileBasename = basename(file)
    try {
        const response = await searchWithAudiotag(env.AUDIOTAG_KEY, file)
        if(response.match){
            const resultsFile = createResultsLog(trimExtension(fileBasename), Mode.AUDIOTAG, `${JSON.stringify(response.match)}\n`)
            try {
                await postWebhook(env.WEBHOOK_URL, `[${Mode.AUDIOTAG}]: ${fileBasename}`, resultsFile)
                success(t('match_found_webhook_sent', { file: fileBasename, mode: Mode.AUDIOTAG }))
            }
            catch(error){
                warning(t('match_found_webhook_failed', { file: fileBasename, error: error.message }))
            }
        }
        else if(response.error)
            warning(t('search_failed', { mode: Mode.AUDIOTAG, file: fileBasename, error: response.error }))
        else
            empty(t('no_match_found', { file: fileBasename, mode: Mode.AUDIOTAG }))
    }
    catch(error){
        warning(t('search_failed', { mode: Mode.AUDIOTAG, file: fileBasename, error: error.message }))
    }
}

async function shazam(env, file){
    const fileBasename = basename(file)
    try {
        await sleep(SHAZAM_SLEEP)
        const { stdout } = await runTool(env.PYTHON_COMMAND, [consts.SHAZAM_SCRIPT, file])
        const result = stdout.trim()
        if(result !== ''){
            const resultsFile = createResultsLog(trimExtension(fileBasename), Mode.SHAZAM, `${result}\n`)
            try {
                await postWebhook(env.WEBHOOK_URL, `[${Mode.SHAZAM}]: ${fileBasename}`, resultsFile)
                success(t('match_found_webhook_sent', { file: fileBasename, mode: Mode.SHAZAM }))
            }
            catch(error){
                warning(t('match_found_webhook_failed', { file: fileBasename, error: error.message }))
            }
        }
        else
            empty(t('no_match_found', { file: fileBasename, mode: Mode.SHAZAM }))
    }
    catch(error){
        warning(t('search_failed', { mode: Mode.SHAZAM, file: fileBasename, error: error.message }))
    }
}

/* ---------------------------------------------------------------------------
 * main
 * ------------------------------------------------------------------------ */

async function init(){
    let { duration, extension, folder, merge, shifts, threads, trim } = argv
    info(t('welcome_message', { version: PROGRAM_VERSION }))
    setupFolders()
    const env = fetchEnvironment()

    if(merge !== undefined){
        await mergeDatabase(env, merge, argv['shard-files'])
        return
    }

    const validatedWebhook = await validateWebhook(env.WEBHOOK_URL)
    if(validatedWebhook){
        env.WEBHOOK_URL = validatedWebhook
        success(t('webhook_set_successfully'))
    }
    const modes = parseModes()
    if(modes.includes(Mode.AUDIOTAG)){
        const validatedAudiotag = await validateAudiotag(env.AUDIOTAG_KEY)
        if(validatedAudiotag){
            env.AUDIOTAG_KEY = validatedAudiotag
            success(t('audiotag_key_set_successfully'))
        }
    }
    if(modes.includes(Mode.MUSICBRAINZ)){
        const validatedMusicbrainz = await validateMusicbrainz(env.ACOUSTID_KEY)
        if(validatedMusicbrainz){
            env.ACOUSTID_KEY = validatedMusicbrainz
            success(t('acoustid_key_set_successfully'))
        }
        extension = validateExtension(extension)
        duration = validateDuration(duration)
    }

    shifts = (!isNaN(shifts) && shifts >= 1 && shifts <= 8) ? Math.floor(shifts) : DEFAULT_QUERY_SHIFTS

    let pklzCount = 0
    if(modes.includes(Mode.AUDFPRINT)){
        threads = Math.min(consts.MAX_CORES_ALLOWED, (!isNaN(threads) && threads > 0) ? threads : availableParallelism())
        pklzCount = setupAudfprint(folder)
    }

    const { audioFiles, precomputedFiles } = loadSamples(modes)
    const prepStartedAt = Date.now()
    const { afpts, mp3s } = await generateFiles(env, trim, shifts, modes, audioFiles, precomputedFiles)
    if(audioFiles.length > 0)
        info(t('input_preparation_took', { duration: formatSeconds(Date.now() - prepStartedAt) }))

    if(modes.some(mode => mode !== Mode.AUDFPRINT)){
        const mp3Modes = modes.filter(mode => mode !== Mode.AUDFPRINT)
        info(t('searching_files_with_modes', { count: mp3s.length, modes: mp3Modes.join(', ') }))
        if(trim > 0)
            info(t('mp3_files_trim_notice', { trim }))
        if(modes.includes(Mode.MUSICBRAINZ)){
            const [minDuration, maxDuration] = duration.split(':').map(Number)
            info(t('musicbrainz_duration_range_notice', { musicbrainz: Mode.MUSICBRAINZ, min: minDuration, max: maxDuration }))
            info(t('musicbrainz_extension_notice', { musicbrainz: Mode.MUSICBRAINZ, extension }))
        }
        for(const mp3 of mp3s){
            const basenameMp3 = basename(mp3)
            if(modes.includes(Mode.MUSICBRAINZ)){
                info(t('searching_file_with_mode', { file: basenameMp3, mode: Mode.MUSICBRAINZ }))
                await musicbrainz(env, mp3, extension, duration)
            }
            if(modes.includes(Mode.AUDIOTAG)){
                info(t('searching_file_with_mode', { file: basenameMp3, mode: Mode.AUDIOTAG }))
                await audiotag(env, mp3)
            }
            if(modes.includes(Mode.SHAZAM)){
                info(t('searching_file_with_mode', { file: basenameMp3, mode: Mode.SHAZAM }))
                await shazam(env, mp3)
            }
        }
    }

    if(modes.includes(Mode.AUDFPRINT)){
        if(afpts.length === 0)
            exit(t('audfprint_need_afpt', { audfprint: Mode.AUDFPRINT }))
        writeFileSync(consts.AFPTS_FILE, afpts.join('\n'))
        info(t('searching_precomputed_files', { count: afpts.length, audfprint: Mode.AUDFPRINT, shifts }))
        info(t('loaded_pklz_total', { count: pklzCount, folder: folder || '' }))
        info(t('using_threads', { count: threads }))
        const matchStartedAt = Date.now()
        await audfprint(env, threads)
        info(t('audfprint_search_completed', {
            audfprint: Mode.AUDFPRINT,
            duration: formatSeconds(Date.now() - matchStartedAt),
            rate: (pklzCount / Math.max(1, (Date.now() - matchStartedAt) / 1000)).toFixed(2)
        }))
        const summary = await createAudfprintLogs(env)
        printAudfprintSummary(summary)
    }

    if(existsSync(RESULTS_FOLDER) && readdirSync(RESULTS_FOLDER).some(file => extname(file) === '.txt'))
        info(t('execution_complete_with_results', { folder: RESULTS_FOLDER }))
    else
        info(t('execution_complete_no_results'))
}

init()

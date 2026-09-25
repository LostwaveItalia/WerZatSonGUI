const dotenv = require('dotenv')
const { exec } = require('node:child_process')
const cluster = require('node:cluster')
const { createReadStream, readFileSync, unlinkSync, writeFileSync } = require('node:fs')
const { basename, join } = require('node:path')
const readline = require('node:readline')
const { promisify } = require('node:util')
const { hideBin } = require('yargs/helpers')
const yargs = require('yargs/yargs')
const consts = require('../utils/consts')
const { t } = require('../utils/i18n')
const { audfprint_info_message } = require('../utils/messages')

dotenv.config()

const execPromise = promisify(exec)
const { argv } = yargs(hideBin(process.argv))

async function matchFingerprint(fingerprint){
    await execPromise(`"${process.env.PYTHON_COMMAND}" "${consts.AUDFPRINT_PROGRAM}" match --min-count 5 --max-matches 75 --search-depth 10000 --dbase "${fingerprint}" --list "${consts.AFPTS_FILE}" >> "${join(consts.TEMP_FOLDER, `${basename(fingerprint)}.match.txt`)}"`)
}

async function storeResults(basenameFingerprint){
    const resultsFile = join(consts.TEMP_FOLDER, `${basenameFingerprint}.match.txt`)
    const fileStream = createReadStream(resultsFile, { encoding: 'utf-8' })
    const results = readline.createInterface({ input: fileStream, crlfDelay: Infinity })
    const matchesMap = {}
    for await(const result of results){
        if(result.startsWith('{')){
            const parsedResult = JSON.parse(result)
            const uniqueKey = `${parsedResult.input_file}:${parsedResult.matched_file}:${basenameFingerprint}`
            if(!matchesMap[uniqueKey])
                matchesMap[uniqueKey] = { ...parsedResult, counter: 1 }
            else {
                if(parsedResult.common_hashes > matchesMap[uniqueKey].common_hashes){
                    matchesMap[uniqueKey].common_hashes = parsedResult.common_hashes
                    matchesMap[uniqueKey].total_hashes = parsedResult.total_hashes
                    matchesMap[uniqueKey].match_time = parsedResult.match_time
                    matchesMap[uniqueKey].rank_position = parsedResult.rank_position
                }
                matchesMap[uniqueKey].counter += 1
            }
        }
    }
    const existingResults = JSON.parse(readFileSync(consts.RESULTS_FILE, 'utf-8'))
    Object.assign(existingResults, matchesMap)
    writeFileSync(consts.RESULTS_FILE, JSON.stringify(existingResults), 'utf-8')
    unlinkSync(resultsFile)
}

if(cluster.isPrimary){
    const { threads } = argv
    writeFileSync(consts.RESULTS_FILE, '{}', 'utf-8')
    const fingerprints = readFileSync(consts.PKLZS_FILE, 'utf-8').trim().split('\n')
    const chunks = Array.from({ length: threads }, () => [])
    fingerprints.forEach((fingerprint, index) => {
        chunks[index % threads].push(fingerprint)
    })
    let completed = 0
    for(let i = 0; i < threads; i++){
        const worker = cluster.fork()
        worker.send({ fingerprints: chunks[i] })
        worker.on('message', async message => {
            if(message.status === 'done'){
                completed += 1
                const basenameFingerprint = basename(message.fingerprint)
                audfprint_info_message(t('analysis_completed', { completed, total: fingerprints.length, basename: basenameFingerprint }))
                await storeResults(basenameFingerprint)
                if(completed === fingerprints.length)
                    process.exit()
            }
        })
    }
}
else {
    process.on('message', async ({ fingerprints }) => {
        for(const fingerprint of fingerprints){
            await matchFingerprint(fingerprint)
            process.send({ status: 'done', fingerprint })
        }
    })
}

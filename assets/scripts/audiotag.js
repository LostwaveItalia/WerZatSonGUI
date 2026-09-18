const FormData = require('form-data')
const { appendFileSync, createReadStream } = require('node:fs')
const { request } = require('undici')
const consts = require('../utils/consts')
const { sleep } = require('../utils/helpers')

const AUDIOTAG_DURATION = 180 // seconds
const AUDIOTAG_SLEEP = 0.5 // seconds
const MAX_AUDIOTAG_ATTEMPTS = 50

const Status = {
    FOUND: 'found',
    NOT_FOUND: 'not found',
    WAIT: 'wait'
}

// Maps the AudioTag API's own "error" strings (see AudioTag-API_v1.0.pdf, Table 2) to a small,
// stable set of codes the rest of the app can branch on, instead of matching raw server text
// all over the place. Matching is a case-insensitive substring test, so small wording additions
// on the server side (e.g. trailing punctuation) don't silently fall through to UNKNOWN.
const ERROR_CODE_MATCHES = [
    ['CREDIT_EXHAUSTED', ['credit balance exhausted', 'credit balance insufficient or exhausted']],
    ['KEY_INVALID', ['api key expired', 'api key inactive', 'api key unrecognized', 'api key invalid or empty']],
    ['TOO_SHORT', ['audio duration is too short']],
    ['BAD_AUDIO', ['audio file: no audio found, format invalid or unsupported']],
    ['SERVER_UNAVAILABLE', ['service temporarily not available']],
    ['INVALID_TOKEN', ['invalid token or no recognition results found for the token']],
    ['BAD_REQUEST', ['invalid command or parameter']]
]

function classifyAudiotagError(rawError){
    if(!rawError)
        return null
    const normalized = String(rawError).toLowerCase()
    if(normalized.includes('internal error'))
        return 'INTERNAL_ERROR'
    const match = ERROR_CODE_MATCHES.find(([, phrases]) => phrases.some(phrase => normalized.includes(phrase)))
    return match ? match[0] : 'UNKNOWN'
}

// Never write a full API key to disk: every log line only ever sees the last 4 characters.
function maskAudiotagKey(key){
    if(!key || key.length < 4)
        return '****'
    return `****${key.slice(-4)}`
}

function logAudiotagDebug(logPath, entry){
    if(!logPath)
        return
    try {
        appendFileSync(logPath, `${JSON.stringify({ timestamp: new Date().toISOString(), ...entry })}\n`)
    }
    catch { /* logging must never break the actual search */ }
}

async function postAudiotag(data, isValidating = false, key = null, actionOverride = null){
    const isToken = typeof data === 'string'
    const action = actionOverride || (isValidating ? 'info' : 'get_result')
    const response = await request(consts.AUDIOTAG_ENDPOINT, {
        method: 'POST',
        headers: isToken ? {
            'Content-Type': 'application/x-www-form-urlencoded'
        } : data.getHeaders(),
        body: isToken ? new URLSearchParams({
            action,
            apikey: key,
            token: actionOverride === 'stat' ? null : (isValidating ? null : data)
        }).toString() : data
    })
    return await response.body.json()
}

// action:stat - fetched once per run (not per track) purely for visibility into the account's
// remaining free-tier budget; see AudioTag-API_v1.0.pdf section 4.2.
async function getAudiotagStat(key, logPath = null){
    try {
        const stat = await postAudiotag('stat', true, key, 'stat')
        logAudiotagDebug(logPath, { phase: 'stat', key: maskAudiotagKey(key), response: stat })
        return stat.success ? stat : null
    }
    catch {
        return null
    }
}

async function searchWithAudiotag(key, file, options = {}){
    const { logPath = null } = options
    const response = { error: null, match: null, resultStatus: null, errorCode: null, rawError: null }
    try {
        const formData = new FormData()
        formData.append('action', 'identify')
        formData.append('apikey', key)
        formData.append('file', createReadStream(file))
        formData.append('start_time', '0')
        formData.append('time_len', AUDIOTAG_DURATION.toString())
        const initialResult = await postAudiotag(formData)
        logAudiotagDebug(logPath, { phase: 'identify', key: maskAudiotagKey(key), file, response: initialResult })

        if(!initialResult.success){
            response.rawError = initialResult.error || null
            response.errorCode = classifyAudiotagError(response.rawError)
            response.resultStatus = 'error'
            return response
        }

        if(initialResult.job_status === Status.FOUND){
            response.match = initialResult.data?.[0]?.tracks?.[0]
            response.resultStatus = response.match ? 'found' : 'not_found'
            return response
        }

        if(initialResult.job_status === Status.WAIT){
            let attempts = 0
            while(attempts < MAX_AUDIOTAG_ATTEMPTS){
                await sleep(AUDIOTAG_SLEEP)
                attempts += 1
                const searchResult = await postAudiotag(initialResult.token, false, key)
                logAudiotagDebug(logPath, { phase: 'get_result', key: maskAudiotagKey(key), file, attempt: attempts, response: searchResult })

                if(!searchResult.success){
                    response.rawError = searchResult.error || null
                    response.errorCode = classifyAudiotagError(response.rawError)
                    response.resultStatus = 'error'
                    return response
                }
                if(searchResult.result !== Status.WAIT){
                    if(searchResult.result === Status.FOUND){
                        response.match = searchResult.data?.[0]?.tracks?.[0]
                        response.resultStatus = response.match ? 'found' : 'not_found'
                    }
                    else
                        response.resultStatus = 'not_found'
                    return response
                }
            }
            response.resultStatus = 'timeout'
            return response
        }

        response.resultStatus = 'not_found'
        return response
    }
    catch(error){
        response.error = error
        response.resultStatus = 'error'
        response.errorCode = 'NETWORK_ERROR'
        logAudiotagDebug(logPath, { phase: 'exception', key: maskAudiotagKey(key), file, error: error.message })
        return response
    }
}

module.exports = { postAudiotag, searchWithAudiotag, getAudiotagStat, classifyAudiotagError, maskAudiotagKey }

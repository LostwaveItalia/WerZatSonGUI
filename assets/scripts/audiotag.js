const FormData = require('form-data')
const { createReadStream } = require('node:fs')
const { request } = require('undici')
const consts = require('../utils/consts')
const { sleep } = require('../utils/helpers')

const AUDIOTAG_DURATION = 180 // seconds
const AUDIOTAG_SLEEP = 0.5 // seconds
const MAX_AUDIOTAG_ATTEMPTS = 50

const Status = {
    FOUND: 'found',
    WAIT: 'wait'
}

async function postAudiotag(data, isValidating = false, key = null){
    const isToken = typeof data === 'string'
    const response = await request(consts.AUDIOTAG_ENDPOINT, {
        method: 'POST',
        headers: isToken ? {
            'Content-Type': 'application/x-www-form-urlencoded'
        } : data.getHeaders(),
        body: isToken ? new URLSearchParams({
            action: isValidating ? 'info' : 'get_result',
            apikey: key,
            token: isValidating ? null : data
        }).toString() : data
    })
    return await response.body.json()
}

async function searchWithAudiotag(key, file){
    const response = { error: null, match: null }
    try {
        const formData = new FormData()
        formData.append('action', 'identify')
        formData.append('apikey', key)
        formData.append('file', createReadStream(file))
        formData.append('start_time', '0')
        formData.append('time_len', AUDIOTAG_DURATION.toString())
        const initialResult = await postAudiotag(formData)
        if(initialResult.success){
            if(initialResult.job_status === Status.FOUND)
                response.match = initialResult.data?.[0]?.tracks?.[0]
            else if(initialResult.job_status === Status.WAIT){
                let attempts = 0
                while(attempts < MAX_AUDIOTAG_ATTEMPTS){
                    await sleep(AUDIOTAG_SLEEP)
                    attempts += 1
                    const searchResult = await postAudiotag(initialResult.token, false, key)
                    if(searchResult.result !== Status.WAIT){
                        response.match = searchResult.result === Status.FOUND ? searchResult.data?.[0]?.tracks?.[0] : null
                        break
                    }
                }
            }
        }
        return response
    }
    catch(error){
        response.error = error
        return response
    }
}

module.exports = { postAudiotag, searchWithAudiotag }

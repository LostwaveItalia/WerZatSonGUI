const dotenv = require('dotenv')
const cluster = require('node:cluster')
const { readFileSync, unlinkSync } = require('node:fs')
const { join } = require('node:path')
const { request } = require('undici')
const { hideBin } = require('yargs/helpers')
const yargs = require('yargs/yargs')
const consts = require('../utils/consts')
const { trimExtension } = require('../utils/helpers')

dotenv.config()

const BLACKLISTED_RESULTS_REGEX = /^94765\d{3}$/
const INTERVAL_DELAY = 600 // milliseconds

const { argv } = yargs(hideBin(process.argv))

async function isBlacklisted(trackId){
    try {
        const { body } = await request(`${consts.ACOUSTID_TRACK_ENDPOINT}/${trackId}`)
        const html = await body.text()
        const matches = [...html.matchAll(/<a\shref="\/fingerprint\/\d+">(\d+)<\/a>/g)]
        if(matches.length > 1)
            return false
        const fingerprintId = matches[0][1]
        return BLACKLISTED_RESULTS_REGEX.test(fingerprintId)
    }
    catch {
        return false
    }
}

async function searchAcoustID(acoustKey, duration, fingerprint){
    const response = { error: false, results: null }
    try {
        const url = new URL(consts.ACOUSTID_LOOKUP_ENDPOINT)
        url.searchParams.append('format', 'json')
        url.searchParams.append('client', acoustKey)
        url.searchParams.append('duration', duration)
        url.searchParams.append('fingerprint', fingerprint)
        const { body } = await request(url.toString())
        const json = await body.json()
        if(json.status !== 'ok'){
            if(json.error?.message === 'invalid API key'){
                console.log(JSON.stringify({ error: true, data: acoustKey }))
                response.error = true
            }
        }
        if(json.status === 'ok' && json.results?.length > 0){
            response.results = await Promise.all(json.results.map(async result => {
                return { result, blacklisted: await isBlacklisted(result.id) }
            }))
            response.results = response.results.filter(({ blacklisted }) => !blacklisted).map(({ result }) => result)
        }
        return response
    }
    catch {
        return response
    }
}

if(cluster.isPrimary){
    const { duration, file } = argv
    const acoustKeys = process.env.ACOUSTID_KEY.split(',')
    const cpuCores = Math.min(consts.MAX_CORES_ALLOWED, acoustKeys.length)
    const [minDuration, maxDuration] = duration.split(':').map(Number)
    const fingerprintsFile = join(consts.TEMP_FOLDER, `${trimExtension(file)}.json`)
    const { fingerprints } = JSON.parse(readFileSync(fingerprintsFile))
    const chunks = Array.from({ length: cpuCores }, () => [])
    Object.keys(fingerprints).forEach((key, index) => {
        chunks[index % cpuCores].push({ [key]: fingerprints[key] })
    })
    let completed = 0
    let matched = false
    for(let i = 0; i < cpuCores; i++){
        const worker = cluster.fork()
        worker.send({
            acoustKey: acoustKeys[i],
            fingerprints: chunks[i],
            maxDuration: maxDuration,
            minDuration: minDuration
        })
        worker.on('message', message => {
            if(message.status === 'match' && !matched){
                matched = true
                for(const id in cluster.workers)
                    cluster.workers[id].kill()
                console.log(JSON.stringify({
                    error: false,
                    data: message.results.map(result => ({
                        trackId: result.id,
                        score: (result.score * 100).toFixed(2),
                        extension: message.key,
                        duration: message.duration
                    }))
                }))
                unlinkSync(fingerprintsFile)
                process.exit()
            }
            else if(message.status === 'done'){
                completed += 1
                if(completed === Object.keys(fingerprints).length){
                    unlinkSync(fingerprintsFile)
                    process.exit()
                }
            }
            else if(message.status === 'quit')
                process.exit()
        })
    }
}
else {
    process.on('message', ({ acoustKey, fingerprints, maxDuration, minDuration }) => {
        let duration = minDuration
        let currentIndex = 0
        let currentKey = Object.keys(fingerprints[currentIndex])[0]
        const interval = setInterval(async () => {
            const response = await searchAcoustID(acoustKey, duration, fingerprints[currentIndex][currentKey])
            if(response.error)
                process.send({ status: 'quit' })
            if(response.results?.length > 0){
                process.send({
                    status: 'match',
                    results: response.results,
                    duration,
                    key: currentKey
                })
            }
            duration += 5
            if(duration >= maxDuration){
                process.send({ status: 'done', key: currentKey })
                currentIndex += 1
                duration = minDuration
                if(currentIndex >= fingerprints.length)
                    clearInterval(interval)
                else
                    currentKey = Object.keys(fingerprints[currentIndex])[0]
            }
        }, INTERVAL_DELAY)
    })
}

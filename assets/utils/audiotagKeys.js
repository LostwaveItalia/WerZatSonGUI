/*
 * Reads WerZatSonGUI's own root config.json for the AudioTag operational settings (cooldown
 * range, rotate/pause-after-N-tracks, pause duration, minimum clip duration, multi-key toggle),
 * the same way utils/i18n.js already reads that file directly for the active language, and
 * manages the on-disk rotation state in audiotag_keys.json.
 *
 * audiotag_keys.json is always the source of truth for per-key usage counters, whether or not
 * multi-key mode is on: with it off, the file is kept in sync with a single entry mirroring
 * env.AUDIOTAG_KEY, so a single-key user still gets the same cooldown/checkpoint-pause
 * bookkeeping (see werzatsong.js's audiotag()) without having to manage a key list themselves.
 */

const { copyFileSync, existsSync, readFileSync, writeFileSync } = require('node:fs')
const consts = require('./consts')

const DEFAULT_SETTINGS = {
    cooldownMinSeconds: 10,
    cooldownMaxSeconds: 30,
    rotateAfterTracks: 100,
    pauseSeconds: 300,
    minDurationSeconds: 15,
    useMultipleKeys: false
}

// Absolute bounds for each AudioTag setting, mirroring the AUDIOTAG_* constants in
// WerZatSonGUI.pyw. A value from config.json outside its window is rejected and replaced
// with the matching default above. Keep these in sync with the Python side.
const AUDIOTAG_BOUNDS = {
    cooldownMinSeconds: { min: 10,  max: 300  },
    cooldownMaxSeconds: { min: 10,  max: 300  },
    rotateAfterTracks:  { min: 100, max: 1000 },
    pauseSeconds:       { min: 60,  max: 3600 },
    minDurationSeconds: { min: 5,   max: 60   }
}

const KeyStatus = {
    OK: 'ok',
    EXHAUSTED: 'exhausted',
    INVALID: 'invalid'
}

function numberOr(value, fallback, bounds){
    const parsed = Number(value)
    if(!Number.isFinite(parsed) || parsed < bounds.min || parsed > bounds.max)
        return fallback
    return parsed
}

function loadSettings(){
    try {
        if(!existsSync(consts.ROOT_CONFIG_FILE))
            return { ...DEFAULT_SETTINGS }
        const raw = JSON.parse(readFileSync(consts.ROOT_CONFIG_FILE, 'utf-8'))
        return {
            cooldownMinSeconds: numberOr(raw.custom_audiotag_cooldown_min_value,
                DEFAULT_SETTINGS.cooldownMinSeconds, AUDIOTAG_BOUNDS.cooldownMinSeconds),
            cooldownMaxSeconds: numberOr(raw.custom_audiotag_cooldown_max_value,
                DEFAULT_SETTINGS.cooldownMaxSeconds, AUDIOTAG_BOUNDS.cooldownMaxSeconds),
            rotateAfterTracks: numberOr(raw.custom_audiotag_rotate_after_tracks_value,
                DEFAULT_SETTINGS.rotateAfterTracks, AUDIOTAG_BOUNDS.rotateAfterTracks),
            pauseSeconds: numberOr(raw.custom_audiotag_pause_seconds_value,
                DEFAULT_SETTINGS.pauseSeconds, AUDIOTAG_BOUNDS.pauseSeconds),
            minDurationSeconds: numberOr(raw.custom_audiotag_min_duration_value,
                DEFAULT_SETTINGS.minDurationSeconds, AUDIOTAG_BOUNDS.minDurationSeconds),
            useMultipleKeys: raw.audiotag_use_multiple_keys === true
        }
    }
    catch {
        return { ...DEFAULT_SETTINGS }
    }
}

function normalizeKeyEntry(entry){
    if(!entry || typeof entry.key !== 'string' || entry.key.trim() === '')
        return null
    return {
        key: entry.key.trim(),
        tracksUsed: Number.isInteger(entry.tracksUsed) && entry.tracksUsed >= 0 ? entry.tracksUsed : 0,
        status: [KeyStatus.OK, KeyStatus.EXHAUSTED, KeyStatus.INVALID].includes(entry.status) ? entry.status : KeyStatus.OK,
        lastError: typeof entry.lastError === 'string' ? entry.lastError : null,
        lastUsedAt: typeof entry.lastUsedAt === 'string' ? entry.lastUsedAt : null
    }
}

function loadRawState(){
    try {
        if(!existsSync(consts.AUDIOTAG_KEYS_FILE)){
            if(existsSync(consts.AUDIOTAG_KEYS_EXAMPLE_FILE))
                copyFileSync(consts.AUDIOTAG_KEYS_EXAMPLE_FILE, consts.AUDIOTAG_KEYS_FILE)
            else
                return { activeIndex: 0, keys: [] }
        }
        const raw = JSON.parse(readFileSync(consts.AUDIOTAG_KEYS_FILE, 'utf-8'))
        const keys = Array.isArray(raw.keys) ? raw.keys.map(normalizeKeyEntry).filter(Boolean) : []
        const activeIndex = Number.isInteger(raw.activeIndex) && raw.activeIndex >= 0 && raw.activeIndex < keys.length ? raw.activeIndex : 0
        return { activeIndex, keys }
    }
    catch {
        return { activeIndex: 0, keys: [] }
    }
}

function saveState(state){
    writeFileSync(consts.AUDIOTAG_KEYS_FILE, JSON.stringify(state, null, 4))
}

function maskKey(key){
    if(!key || key.length < 4)
        return '****'
    return `****${key.slice(-4)}`
}

class AudiotagKeyManager {
    constructor(settings, state){
        this.settings = settings
        this.state = state
        this.disabledForRun = false
    }

    hasUsableKey(){
        return this.state.keys.some(entry => entry.status === KeyStatus.OK)
    }

    getActiveKey(){
        const current = this.state.keys[this.state.activeIndex]
        if(current && current.status === KeyStatus.OK)
            return current
        return this._advanceToNextUsable()
    }

    _advanceToNextUsable(){
        const usableIndex = this.state.keys.findIndex(entry => entry.status === KeyStatus.OK)
        if(usableIndex === -1)
            return null
        this.state.activeIndex = usableIndex
        saveState(this.state)
        return this.state.keys[usableIndex]
    }

    recordTrackUsage(key){
        const entry = this.state.keys.find(item => item.key === key)
        if(!entry)
            return
        entry.tracksUsed += 1
        entry.lastUsedAt = new Date().toISOString()
        saveState(this.state)
    }

    markKeyStatus(key, status, errorMessage = null){
        const entry = this.state.keys.find(item => item.key === key)
        if(!entry)
            return
        entry.status = status
        entry.lastError = errorMessage
        saveState(this.state)
    }

    // Advances to the next usable key after the currently active one (wrapping around),
    // returning it, or null when no other usable key exists.
    rotateToNextKey(){
        if(this.state.keys.length === 0)
            return null
        const startIndex = this.state.activeIndex
        for(let offset = 1; offset <= this.state.keys.length; offset++){
            const candidate = (startIndex + offset) % this.state.keys.length
            if(this.state.keys[candidate].status === KeyStatus.OK){
                this.state.activeIndex = candidate
                saveState(this.state)
                return this.state.keys[candidate]
            }
        }
        return null
    }

    // True once the given key has processed a multiple of rotateAfterTracks tracks - checked
    // BEFORE each request, so it fires exactly once per checkpoint regardless of which
    // werzatsong.js invocation (the GUI runs one per sub-30-file batch) happens to be running
    // when the threshold is crossed.
    isCheckpoint(key){
        const entry = this.state.keys.find(item => item.key === key)
        const tracksUsed = entry ? entry.tracksUsed : 0
        return tracksUsed > 0 && tracksUsed % this.settings.rotateAfterTracks === 0
    }
}

// Builds the manager for a run. In single-key mode, audiotag_keys.json is silently reset to
// hold exactly one entry mirroring envKey (preserving its counters if it already matches),
// so switching .env keys doesn't carry over a stale, unrelated usage count.
function createAudiotagKeyManager(envKey){
    const settings = loadSettings()
    let state = loadRawState()

    if(!settings.useMultipleKeys){
        const trimmedEnvKey = (envKey || '').trim()
        const existing = state.keys.find(entry => entry.key === trimmedEnvKey)
        state = {
            activeIndex: 0,
            keys: trimmedEnvKey ? [existing || normalizeKeyEntry({ key: trimmedEnvKey })] : []
        }
        saveState(state)
    }

    return new AudiotagKeyManager(settings, state)
}

module.exports = { createAudiotagKeyManager, KeyStatus, maskKey, loadSettings }

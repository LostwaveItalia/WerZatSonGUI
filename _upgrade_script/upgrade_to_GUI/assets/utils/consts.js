const { join } = require('node:path')

const ROOT_PATH = join(__dirname, '..')

const consts = {
    // Limits
    MAX_CORES_ALLOWED: 16, // avoid out of memory error
    // Endpoints
    ACOUSTID_LOOKUP_ENDPOINT: 'https://api.acoustid.org/v2/lookup',
    ACOUSTID_TRACK_ENDPOINT: 'https://acoustid.org/track',
    AUDIOTAG_ENDPOINT: 'https://audiotag.info/api',
    // Folders
    // WERZATSONG_DATABASE_DIR / WERZATSONG_LOGS_DIR let WerZatSonGUI (or any other
    // launcher) relocate these two folders without touching this file's defaults
    DATABASE_FOLDER: process.env.WERZATSONG_DATABASE_DIR || join(ROOT_PATH, 'database'),
    INPUT_FOLDER: join(ROOT_PATH, 'input'),
    LOGS_FOLDER: process.env.WERZATSONG_LOGS_DIR || join(ROOT_PATH, 'logs'),
    PRECOMPUTED_FOLDER: join(ROOT_PATH, 'precomputed'),
    PROCESSED_FOLDER: join(ROOT_PATH, 'processed'),
    TEMP_FOLDER: join(ROOT_PATH, 'temp'),
    // Files
    AFPTS_FILE: join(ROOT_PATH, 'temp', '_afpts.txt'),
    AUDFPRINT_PROGRAM: join(ROOT_PATH, 'libs', 'audfprint', 'audfprint.py'),
    AUDFPRINT_SCRIPT: join(ROOT_PATH, 'scripts', 'audfprint.js'),
    ENV_FILE: join(ROOT_PATH, '.env'),
    EXAMPLE_ENV_FILE: join(ROOT_PATH, '.env.example'),
    FILLER_FILE: join(ROOT_PATH, 'resources', 'filler.mp3'),
    FPCALC_SCRIPT: join(ROOT_PATH, 'scripts', 'fpcalc.js'),
    MUSICBRAINZ_SCRIPT: join(ROOT_PATH, 'scripts', 'musicbrainz.js'),
    PKLZS_FILE: join(ROOT_PATH, 'temp', '_pklzs.txt'),
    RESULTS_FILE: join(ROOT_PATH, 'temp', '_results.json'),
    SHAZAM_SCRIPT: join(ROOT_PATH, 'scripts', 'shazam.py')
}

module.exports = consts

/*
 * Loads werzatsong.js's console translations. The active language comes from config.json
 * (kept in sync by WerZatSonGUI.pyw's own Language setting), so running werzatsong.js
 * through the GUI automatically follows whatever language it's currently set to. Falls
 * back to English whenever config.json is missing/unreadable/invalid, so the script still
 * works fine when run standalone, outside of the GUI.
 */

const { existsSync, readFileSync } = require('node:fs')
const { join } = require('node:path')

const CONFIG_FILE = join(__dirname, '..', '..', 'config.json')
const LOCALIZATIONS_FOLDER = join(__dirname, '..', 'localizations')

function loadLanguage(){
    try {
        if(!existsSync(CONFIG_FILE))
            return 'English'
        const raw = JSON.parse(readFileSync(CONFIG_FILE, 'utf-8'))
        return raw.language === 'Italiano' ? 'Italiano' : 'English'
    }
    catch {
        return 'English'
    }
}

function loadTranslations(language){
    const fileName = language === 'Italiano' ? 'console_strings_Italiano.json' : 'console_strings_English.json'
    const filePath = join(LOCALIZATIONS_FOLDER, fileName)
    try {
        return JSON.parse(readFileSync(filePath, 'utf-8'))
    }
    catch {
        return {}
    }
}

const translations = loadTranslations(loadLanguage())

function t(key, vars = {}){
    let template = translations[key]
    if(template === undefined)
        template = key
    for(const [name, value] of Object.entries(vars))
        template = template.split(`{${name}}`).join(String(value))
    return template
}

module.exports = { t }

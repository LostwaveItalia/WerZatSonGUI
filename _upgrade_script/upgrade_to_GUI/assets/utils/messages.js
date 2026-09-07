const { cyan, gray, greenBright, redBright, yellow } = require('chalk')
const { t } = require('./i18n')

const Message = {
    EMPTY: gray,
    ERROR: redBright,
    INFO: cyan,
    SUCCESS: greenBright,
    WARNING: yellow
}

function empty(message){
    console.log(Message.EMPTY(`[${t('tag_empty')}]: ${message}`))
}

function exit(message){
    console.error(Message.ERROR(`[${t('tag_error')}]: ${message}`))
    process.exit(1)
}

function info(message){
    console.log(Message.INFO(`[${t('tag_info')}]: ${message}`))
}

function success(message){
    console.log(Message.SUCCESS(`[${t('tag_success')}]: ${message}`))
}

function warning(message){
    console.log(Message.WARNING(`[${t('tag_warning')}]: ${message}`))
}

function audfprint_info_message(message){
    console.log(Message.INFO(`${message}`))
}

module.exports = { empty, exit, info, success, warning, audfprint_info_message }

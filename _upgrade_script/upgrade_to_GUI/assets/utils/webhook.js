const FormData = require('form-data')
const { existsSync, readFileSync } = require('node:fs')
const { basename } = require('node:path')
const { request } = require('undici')

const WEBHOOK_AVATAR = 'https://cdn.discordapp.com/app-icons/1509584409748050011/5136222148bbb7541919a2e5c89924f1.webp'
const WEBHOOK_USERNAME = 'WerZatSonGUI'

async function postWebhook(url, content, filePath = null){
    try {
        let formData = null
        if(filePath && existsSync(filePath)){
            formData = new FormData()
            formData.append('content', content)
            formData.append('username', WEBHOOK_USERNAME)
            formData.append('avatar_url', WEBHOOK_AVATAR)
            formData.append('file', readFileSync(filePath), {
                filename: basename(filePath),
                contentType: 'text/plain'
            })
        }
        const { statusCode } = await request(url, {
            method: 'POST',
            headers: filePath ? formData.getHeaders() : {
                'Content-Type': 'application/json'
            },
            body: filePath ? formData : JSON.stringify({
                content,
                username: WEBHOOK_USERNAME,
                avatar_url: WEBHOOK_AVATAR
            })
        })
        return statusCode >= 200 && statusCode < 300
    }
    catch {
        return false
    }
}

module.exports = postWebhook

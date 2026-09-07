function generateUnique(){
    return new Date().toISOString().replace('T', '_').split('.')[0].replace(/:/g, '-')
}

function sleep(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000))
}

function trimExtension(filename){
    return filename.split('.').slice(0, -1).join('.')
}

module.exports = { generateUnique, sleep, trimExtension }

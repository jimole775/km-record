const childProcess = require('child_process')
const readline = require('readline')
const fs = require('fs')

// type = 'version' | 'tag'
const type = getCMDParams()

switch (type) {
  case 'version':
    updateVersion()
    break
  case 'tag':
    makeTag()
    break
  default:
    makeTag()
    break
}

function makeTag () {
  getCurrentVersion().then((version) => {
    version = queryVersion(version)
    const date = getDate()
    childProcess.exec(`git tag -a v${version} -m "${date}"`)
  })
}

function updateVersion () {
  const tmpStream = fs.createWriteStream('./package.tmp.json')
  const packageStream = fs.createReadStream('./package.json')
  const rl = readline.createInterface({
    input: packageStream,
    console: false
  })
  rl.on('line', function (line) {
    const vMatch = /\"version\": ?(\"\d\.\d{1,}\.\d{1,}\"),/ig
    if (vMatch.test(line)) {
      const nextV = growVersion(line.replace(vMatch, '$1'))
      tmpStream.write(`  "version": "${nextV}",\r\n`)
    } else {
      tmpStream.write(line + '\r\n')
    }
  })
  rl.on('close', function () {
    tmpStream.close()
    replacePackageFile()
  })
}

function growVersion (v) {
  v = queryVersion(v)
  let mainV = Number.parseInt(v.split('.')[0])
  let midV = Number.parseInt(v.split('.')[1])
  let chunkV = Number.parseInt(v.split('.')[2])
  chunkV = chunkV + 1
  if (chunkV > 99) {
    chunkV = 1
    midV = midV + 1
  }
  if (midV > 9) {
    midV = 1
    mainV = mainV + 1
  }
  return `${mainV}.${midV}.${chunkV}`
}

function getCurrentVersion () {
  return new Promise((resolve, reject) => {
    const packageStream = fs.createReadStream('./package.json')
    const rl = readline.createInterface({
      input: packageStream,
      console: false
    })
    rl.on('line', function (line) {
      const vMatch = /\"version\": ?(\"\d\.\d{1,}\.\d{1,}\"),/ig
      if (vMatch.test(line)) {
        resolve(line.replace(vMatch, '$1'))
        rl.close()
      }
    })
  })
}

function replacePackageFile () {
  return new Promise(function (resolve, reject) {
    try {
      fs.unlinkSync('./package.json')
      fs.renameSync('./package.tmp.json', './package.json')
      resolve()
    } catch (error) {
      reject(error)
      console.log(error)
    }
  })
}

function getCMDParams () {
  let res = ''
  if (process.argv && process.argv.length) {
    process.argv.forEach((item) => {
      if (item && /^\-\-.+/.test(item)) {
        res = item.replace(/\-\-/g, '')
      }
    })
  }
  return res
}

function queryVersion (v) {
  v = v ? v.trim() : v
  v = /\"/.test(v) ? v.replace(/\"/g, '') : v
  return v
}

function getDate () {
  const date = new Date()
  const yyyy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return `${yyyy}-${mm}-${dd}`
}

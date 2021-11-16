const fs = require('fs')
const path = require('path')
const thePath = path.join(__dirname, 'dist/index.html')
fs.readFile(thePath, (err, data) => {
  if (err) throw err;
  const tarPath = path.join(__dirname, 'dist/js').replace(/\\/g, '/')
  const dirty = data.toString()
  const pure = dirty.replace(/href=\//ig, 'href=').replace(/src=\//ig, 'src=')
  let reg = new RegExp(`<link href=${tarPath}(.*?)\.js rel=prefetch>`, 'ig')
  let res = pure.replace(reg, `<script src=${tarPath}$1.js></script>`)
  reg = new RegExp(`<link href=${tarPath}(.*?)\.js rel=preload as=script>`, 'ig')
  res = res.replace(reg, `<script src=${tarPath}$1.js></script>`)
  fs.writeFile(thePath, res, () => {})
})

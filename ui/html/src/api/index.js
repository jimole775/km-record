const context = require.context('./modules', true, /(\.js)$/)
let api = {}
context.keys().forEach((item) => {
  api = Object.assign(api, context(item).default || context(item))
})

export default { ...api }

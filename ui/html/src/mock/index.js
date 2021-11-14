import mock from 'mockjs'
import store from '@/store'
import utils from '../utils'
const context = require.context('./', true, /(\.js)$/)
const apiBase = 'mock'
context.keys().forEach((item) => {
  const fileName = item.replace(/^\.[\\\/]/g, '').replace(/(\.js)$/g, '')
  const data = context(item).default || context(item)
  const reg = new RegExp(`\\/${apiBase}\\/${fileName}\\??\\w*?`, 'i')
  mock.mock(reg, options => {
    const params = getParams(options)
    return dataQuery(mock.mock(data), params)
  })
})

function getParams (options) {
  let res = null
  if (options.type === 'GET' && utils.hasQueryString(options.url)) {
    res = utils.getParamsFromURL(options.url)
  }
  if (options.body) {
    res = utils.isJSONString(options.body) ? JSON.parse(options.body) : options.body
  }
  return res
}

function dataQuery (data, params) {
  let res = utils.clone(data)
  if (params && res.data) {
    if (utils.isArray(params)) {
      // 暂时没有这种查询需求
    }
    if (utils.isObject(params) && utils.isArray(res.data)) {
      res.data = res.data.filter((row) => {
        const rowKeyMark = {}
        Object.keys(params).forEach((key) => {
          // 如果数据中没有这个字段
          // 可以判断这个是一个无效的查询字段
          if (!row.hasOwnProperty(key)) {
            return false
          }
          const queryMark = params[key]
          if (queryMark) {
            const sourceString = row[key]
            if (utils.isValuable(sourceString)) {
              if (utils.isDateString(sourceString) && utils.isDateString(queryMark)) {
                // 过滤时间
                rowKeyMark[key] = hasInDateRange(key, row, params)
              } else if (utils.isString(sourceString)) {
                // 过滤字符
                rowKeyMark[key] = sourceString.indexOf((queryMark + '')) === 0
              } else if (utils.isNumber(sourceString)) {
                // 过滤数字
                rowKeyMark[key] = (sourceString + '').indexOf((queryMark + '')) === 0
              } else {
                // params的查询字段有值，但是匹配不到类型，过滤
                rowKeyMark[key] = false
              }
            } else {
              // row的这个字段没有值，过滤
              rowKeyMark[key] = false
            }
          } else {
            // params的查询字段没有值，不过滤
            rowKeyMark[key] = true
          }
        })
        return shouldShowThisRow(rowKeyMark)
      })
    }
  }
  return res
}

function shouldShowThisRow (rowKeyMark) {
  let res = true
  const keys = Object.keys(rowKeyMark)
  for (let i = 0; i < keys.length; i++) {
    const key = keys[i]
    if (!rowKeyMark[key]) {
      res = false
      break
    }
  }
  return res
}

function hasInDateRange (key, row, params) {
  const moment = utils.moment
  const sourceString = row[key]
  const queryMark = params[key]
  const { start, end } = getRangeField(key, params)
  if (start && end) {
    const rStart = moment(row[start])
    const pStart = moment(params[start])
    const rEnd = moment(row[end])
    const pEnd = moment(params[end])
    return (rStart >= pStart) && (rEnd <= pEnd)
  } else if (key.includes('year')) {
    return moment(sourceString).format('YYYY') === moment(queryMark).format('YYYY')
  } else if (key.includes('month')) {
    return moment(sourceString).format('MM') === moment(queryMark).format('MM')
  } else {
    return moment(sourceString) === moment(queryMark)
  }
}

function getRangeField (key, params) {
  let res = {}
  if (key.includes('end') || key.includes('start')) {
    Object.keys(params).forEach((k) => {
      if (k.includes('start')) {
        res['start'] = k
      }
      if (k.includes('end')) {
        res['end'] = k
      }
    })
  }
  return res
}

mock.setup(500)

store.commit('setMockEnv', true)

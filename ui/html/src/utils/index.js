import moment from 'moment'
import 'moment/locale/zh-cn'
import { cloneDeep, merge, debounce } from 'lodash'
import { Modal } from 'ant-design-vue'
import axios from 'axios'
import { getToken } from './auth'
import store from '@/store'
import base64 from './base64'
moment.locale('zh-cn')
const utils = {
  moment,
  debounce,
  date2Y (strOrDate) {
    return this.isValuable(strOrDate) ? moment(strOrDate).format('YYYY') : ''
  },
  date2M (strOrDate) {
    return this.isValuable(strOrDate) ? moment(strOrDate).format('MM') : ''
  },
  date2YM (strOrDate, splitSign = '-') {
    return this.isValuable(strOrDate) ? moment(strOrDate).format(`YYYY${splitSign}MM`) : ''
  },
  date2HM (strOrDate) {
    return this.isValuable(strOrDate) ? moment(strOrDate).format('HH:mm') : ''
  },
  date2YMD (strOrDate, splitSign = '-') {
    return this.isValuable(strOrDate) ? moment(strOrDate).format(`YYYY${splitSign}MM${splitSign}DD`) : ''
  },
  date2YMDH (strOrDate, splitSign = '-') {
    return this.isValuable(strOrDate) ? moment(strOrDate).format(`YYYY${splitSign}MM${splitSign}DD HH`) : ''
  },
  date2YMDHM (strOrDate, splitSign = '-') {
    return this.isValuable(strOrDate) ? moment(strOrDate).format(`YYYY${splitSign}MM${splitSign}DD HH:mm`) : ''
  },
  /**
   * @param {string} input value
   * @returns {number} output value
   */
  byteLength (str) {
    // returns the byte length of an utf8 string
    let s = str.length
    for (var i = str.length - 1; i >= 0; i--) {
      const code = str.charCodeAt(i)
      if (code > 0x7f && code <= 0x7ff) s++
      else if (code > 0x7ff && code <= 0xffff) s += 2
      if (code >= 0xDC00 && code <= 0xDFFF) i--
    }
    return s
  },
  findPathDFS (source, goal) {
    if (!this.isArray(source)) {
      return []
    }
    // 因为会改变原数据，因此做深拷贝处理
    var dataSource = JSON.parse(JSON.stringify(source))
    var res = []
    return (function dfs (data) {
      res.push(data)
      // 深度搜索一条数据，存取在数组 res 中
      if (data.children) return dfs(data.children[0])
      // 匹配成功
      if (res[res.length - 1].path === goal) {
        return res
      }
      // 匹配失败则删掉当前比对的节点
      res.pop()
      // 没有匹配到任何值则 return，如果源数据有值则再次深度搜索
      if (!res.length) return dataSource.length > 0 ? dfs(dataSource.shift()) : res
      // 取得最后一个节点，待做再次匹配
      var lastNode = res[res.length - 1]
      // 删除已经匹配失败的节点（即为上面 res.pop() 的内容）
      lastNode.children.shift()
      // 没有 children 时
      if (!lastNode.children.length) {
        // 删除空 children，且此时需要深度搜索的为 res 的最后一个值
        delete lastNode.children
        return dfs(res.pop())
      }
      return dfs(lastNode.children[0])
    })(dataSource.shift())
  },
  /**
   * 根据后台返回的数据，生成分页配置信息
   * @param {} res
   */
  getPaginationConfig (res) {
    if (this.isEmpty(res)) {
      return {
        defaultCurrent: 1,
        defaultPageSize: 20,
        showTotal: total => `共 ${total} 条`,
        showSizeChanger: true,
        pageSizeOptions: ['10', '20', '50', '100']
      }
    }
    return {
      current: 'pageNum' in res ? res.pageNum + 1 : 'number' in res ? res.number + 1 : 1,
      pageSize: res.pageSize || res.size,
      total: res.totalElements || res.total,
      showTotal: total => `共 ${total} 条`
    }
  },
  getPaginationConfig2 (res) {
    if (this.isEmpty(res)) {
      return {
        defaultCurrent: 1,
        defaultPageSize: 10,
        showTotal: total => `共 ${total} 条`,
        showSizeChanger: true,
        pageSizeOptions: ['10', '20', '50', '100']
      }
    }
    return {
      current: 'pageNum' in res ? res.pageNum : 'number' in res ? res.number : 1,
      pageSize: res.pageSize || res.size,
      total: res.totalElements || res.total,
      showTotal: total => `共 ${total} 条`
    }
  },
  getPaginationConfig3 (res) {
    if (this.isEmpty(res)) {
      return {
        defaultCurrent: 1,
        defaultPageSize: 10,
        showTotal: total => `共 ${total} 条`
      }
    }
    if (!res.content.length) {
      return {
        current: 1,
        pageSize: 10,
        showSizeChanger: false,
        total: 0,
        showTotal: total => `共 ${total} 条`
      }
    }
    return {
      current: res.pageNum + 1 || res.number + 1 || 1,
      pageSize: res.pageSize || res.size,
      showSizeChanger: true,
      total: res.totalElements || res.total,
      showTotal: total => `共 ${total} 条`
    }
  },
  resetPagination (queryObj) {
    queryObj.current = 1
    queryObj.pageSize = 10
    queryObj.showSizeChanger = true
    queryObj.pageSizeOptions = ['10', '20', '50', '100']
    return queryObj
  },
  filterInvalidDate (obj) {
    for (let k in obj) {
      if (obj[k] === 'Invalid date') {
        obj[k] = ''
      }
    }
    return obj
  },
  /** 拼装 UserSelect 的输入项
   * @params ids => 'xxx,xxx'
   * @params names => 'xxx,xxx'
   * @return [{label: '', key: ''},{label: '', key: ''}]
   */
  parseUser (ids, names) {
    const userList = []
    if (ids && names) {
      const namesList = names.split(',')
      ids.split(',').forEach((item, index) => {
        userList.push({
          label: `${item} ${namesList[index]}`,
          key: JSON.stringify({ key: item, label: namesList[index] })
        })
      })
    }
    return userList
  },
  /** 拆分 UserSelect 的输入项
   * @params list => [{label: '', key: ''},{label: '', key: ''}]
   * @return ['num1, num2', 'name1, name2']
   */
  splitUser (list) {
    if (this.isEmpty(list)) {
      return ['', '']
    }
    const listTemp = list.map(item => {
      return JSON.parse(item.key)
    })

    return [listTemp.map(item => {
      return item.key
    }).join(','), listTemp.map(item => {
      return item.label
    }).join(',')]
  },
  // 切割解析URL地址，主要用于Uploader组件的
  splitUrl (url) {
    if (this.isEmpty(url)) {
      return {
        domain: '', // 域名
        fileName: '', // 文件名
        path: '' // 文件地址path
      }
    }
    const urlObjList = url.split('/')
    let obj = {
      domain: urlObjList[0] + '//' + urlObjList[2],
      fileName: urlObjList[urlObjList.length - 1],
      path: '/' + urlObjList.slice(3).join('/')
    }
    return obj
  },
  // 证件号码，预留前后4位，其他隐藏
  formatCertificateNo (val) {
    const res = []
    val && val.split('').forEach((word, index) => {
      if (index < 4 || index >= val.length - 4) {
        res.push(word)
      } else {
        res.push('*')
      }
    })
    return res.join('')
  },
  /**
   * 数字转金钱
   * @param {Number|String} number 输入数字
   * @param {Number} decimals 保留的小数位，默认 2
   * @param {Number} decPoint 小数点符号
   * @param {Number} thousandsSep 千分位符号
   * @return {String}
   * @template = number2money(1234) => '123,4.00'
   * @template = number2money(1234, 3) => '123,4.000'
   */
  number2money (number, decimals, decPoint, thousandsSep) {
    number = (number + '').replace(/[^0-9+-Ee.]/g, '')
    var n = !isFinite(+number) ? 0 : +number
    var prec = !isFinite(+decimals) ? 0 : Math.abs(decimals)
    var sep = (typeof thousandsSep === 'undefined') ? ',' : thousandsSep
    var dec = (typeof decPoint === 'undefined') ? '.' : decPoint
    var s = ''
    var toFixedFix = function (n, prec) {
      var k = Math.pow(10, prec)
      return '' + Math.round(n * k) / k
    }
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.')
    var re = /(-?\d+)(\d{3})/
    while (re.test(s[0])) {
      s[0] = s[0].replace(re, '$1' + sep + '$2')
    }
    if ((s[1] || '').length < prec) {
      s[1] = s[1] || ''
      s[1] += new Array(prec - s[1].length + 1).join('0')
    }
    return s.join(dec)
  },
  /**
   * 金钱转数字
   * @param {Number|String} input
   * @return {String}
   * @template = money2number('') => ''
   * @template = money2number(12334) => '12334'
   * @template = money2number('123,234') => '123234'
   */
  money2number (input) {
    if (!input) return input
    return Number.parseFloat((input + '').replace(/,/g, ''))
  },
  /** 把对象转换成的urlquery字段
   * @param {String}
   * @return {Boolean}
   * @template = hasQueryString('?dasd') => true
   * @template = hasQueryString('?dasd=1') => true
   * @template = hasQueryString('/sdad?') => false
   * @template = hasQueryString('') => false
   * @template = hasQueryString('?') => false
   */
  hasQueryString (src) {
    if (!src) return false
    if (!this.isString(src)) return false
    return /\w*?\?{1}\w+/.test(src)
  },
  /** 把对象转换成的urlquery字段
   * @param {Object} obj
   * @return {String}
   * @template = setParamsToURL({a: 1}) => '?a=1'
   * @template = setParamsToURL({a: ''}) => ''
   * @template = setParamsToURL({}) => ''
   */
  setParamsToURL (obj) {
    if (!this.isObject(obj)) return new Error('utils.toQueryString参数必须是Object类型')
    const res = []
    Object.keys(obj).forEach(key => {
      const val = obj[key]
      if (this.isValuable(val)) {
        res.push(`${key}=${encodeURIComponent(val)}`)
      }
    })
    return res.length ? `?${res.join('&')}` : ``
  },
  /** 把urlquery转换成的Object对象
   * @param {String} url
   * @return {Object}
   * @template = getParamsFromURL('') => { }
   * @template = getParamsFromURL('?') => { }
   * @template = getParamsFromURL('&') => { }
   * @template = getParamsFromURL('/xxx/xxx') => { }
   * @template = getParamsFromURL('xxx=xxx') => { xxx: xxx }
   * @template = getParamsFromURL('&xxx=xxx') => { xxx: xxx }
   * @template = getParamsFromURL('?xxxx=xxx&xxx=xxx') => { xxxx: xxx, xxx: xxx }
   * @template = getParamsFromURL('/xxx/xxx?xxxx=xxx&xxx=xxx') => { xxxx: xxx, xxx: xxx }
   */
  getParamsFromURL (url) {
    if (!url) return {}
    if (!/[&\?]/g.test(url)) return {}
    const paramPartString = url.split('?')[1]
    if (!paramPartString) return {}
    const params = paramPartString.split('&')
    const res = {}
    params.forEach((item) => {
      if (/\=/.test(item)) {
        const tmp = item.split('=')
        res[tmp[0]] = tmp[1]
      }
    })
    return res
  },
  verifyUploadType (fileName, supportSeries) {
    if (!fileName) {
      Modal.warning({
        title: '上传失败',
        content: '请上传正确的文件！'
      })
      return false
    }

    if (!/\./.test(fileName)) {
      Modal.warning({
        title: '上传失败',
        content: '检测不到文件类型，请重新选择！'
      })
      return false
    }

    const type = fileName.split('.').pop()
    if (!type) {
      Modal.warning({
        title: '上传失败',
        content: '检测不到文件类型，请重新选择！'
      })
      return false
    }

    if (supportSeries && !supportSeries.includes('.' + type)) {
      Modal.warning({
        title: '上传失败',
        content: `文件类型不正确，请重新选择！当前支持的类型：${supportSeries.replace(/,/g, ' ')}。`
      })
      return false
    }

    return true
  },
  /** 直接访问CDN服务器，以link的方式来下载文件
   * @param {String} url url为文件的全路径
   * @param {Object} param 额外参数
   * @param {String} customFileName 自定义文件名
   * @return {Undefined}
   * @template = downloadFileByLink('xxx/xxx.xx') => Undefined
   * @template = downloadFileByLink('xxx/xxx.xx', {xx: x}) => Undefined
   * @template = downloadFileByLink('xxx/xxx.xx?xxx=xxx', {xx: x}) => Undefined
   * @template = downloadFileByLink('xxx/xxx.xx?xxx=xxx', {xx: x}, '文件名') => Undefined
   */
  downloadFileByLink (url, param = {}, customFileName) {
    if (!url) return new Error('url不能为空！')
    let domain = window.location.origin
    if (store.getters.getCurrentDomain) {
      domain = store.getters.getCurrentDomain()
    }
    const link = document.createElement('a')
    const fileName = customFileName || (url.indexOf('/') !== -1 ? url.split('/')[url.split('/').length - 1] : 'unknowFile')
    const fileUrl = `${domain}${this.encodeFileName(url.split('?')[0])}`
    const fileParam = `${this.setParamsToURL({ ...this.getParamsFromURL(url), ...param, auth_token: `oms:${getToken()}` })}`
    link.style.display = 'none'
    link.href = fileUrl + fileParam
    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  },
  /** 直接访问CDN服务器，通过二进制流的方式下载文件
   * @param {String} url url为文件的全路径
   * @param {String} customFileName 自定义文件名
   * @return {Undefined}
   * @template = downloadFileByStream('/xxx/xxx.xx') => Undefined
   * @template = downloadFileByStream('/xxx/xxx.xx?xxx=xxx', 'xxx.xx') => Undefined
   */
  downloadFileByStream (url, customFileName) {
    if (!url) return new Error('url不能为空！')
    let domain = window.location.origin
    if (store.getters.getCurrentDomain) {
      domain = store.getters.getCurrentDomain()
    }
    axios({
      method: 'get',
      url: `${domain}${this.encodeFileName(url.split('?')[0])}`,
      params: {
        ...this.getParamsFromURL(url),
        auth_token: `oms:${getToken()}`
      },
      responseType: 'blob'
    }).then(res => {
      if (res.code) {
        return
      }
      const link = document.createElement('a')
      const blob = new Blob([res.data], { type: 'application/octet-stream' })
      const fileName = decodeURI(url).split('/').pop() || 'unknowFile'
      link.style.display = 'none'
      link.href = URL.createObjectURL(blob)
      link.setAttribute('download', customFileName || fileName)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    })
      .catch(() => {
        console.log('失败')
      })
  },
  /** 通过后端接口的方式，来下载文件
   * @param {String} url url一般带有api路段
   * @param {Object} params
   * @return {Promise[*]}
   * @template = exportGetFile('/api/xxx/xxx') => Promise
   * @template = exportGetFile('/api/xxx/xxx', {xx: x}) => Promise
   * @template = exportGetFile('/api/xxx/xxx.xx?xxx=xxx', {xx: x}) => Promise
   */
  exportGetFile (url, obj) {
    return new Promise(async (resolve, reject) => {
      const res = await axios({
        method: 'get',
        url: url,
        params: obj,
        responseType: 'blob',
        headers: {
          'x-token': getToken()
        }
      }).catch((error) => {
        console.log(error)
        return reject(error)
      })
      // 如果是后台数据，需要直接返回res
      if (this.isBackendResponse(res)) return resolve(res)
      // 如果是axios数据，需要判断内部结构
      if (this.isAxiosResponse(res)) {
        let backendData = res.data
        if (this.isBlob(backendData)) {
          backendData = await this.readBlobAsText(backendData)
        }
        if (this.isJSONString(backendData)) {
          backendData = JSON.parse(backendData)
        }
        if (this.isBackendResponse(backendData)) {
          return resolve(backendData)
        } else {
          this.blobToURI(res)
          return resolve(true)
        }
      }
    })
  },
  /** 通过后端接口的方式，来下载文件
   * @param {String} url url一般带有api路段
   * @param {Object} params
   * @return {Promise[*]}
   * @template = exportPostFile('/api/xxx/xxx') => Promise
   * @template = exportPostFile('/api/xxx/xxx', {xx: x}) => Promise
   * @template = exportPostFile('/api/xxx/xxx.xx?xxx=xxx', {xx: x}) => Promise
   */
  exportPostFile (url, params) {
    return new Promise(async (resolve, reject) => {
      const res = await axios({
        method: 'post',
        url: url,
        data: params,
        responseType: 'blob',
        headers: {
          'x-token': getToken()
        }
      }).catch((error) => {
        console.log(error)
        return reject(error)
      })
      // 如果是后台数据，需要直接返回res
      if (this.isBackendResponse(res)) return resolve(res)
      // 如果是axios数据，需要判断内部结构
      if (this.isAxiosResponse(res)) {
        let backendData = res.data
        if (this.isBlob(backendData)) {
          backendData = await this.readBlobAsText(backendData)
        }
        if (this.isJSONString(backendData)) {
          backendData = JSON.parse(backendData)
        }
        if (this.isBackendResponse(backendData)) {
          return resolve(backendData)
        } else {
          this.blobToURI(res)
          return resolve(true)
        }
      }
    })
  },
  blobToURI (res) {
    const link = document.createElement('a')
    const blob = new Blob([res.data], { type: 'application/octet-stream' })
    const disposition = res.headers['content-disposition'] || ''
    const fileField = disposition.split(';')[1] || ''
    const fileName = decodeURI(fileField.split('=')[1] || 'unname')
    link.style.display = 'none'
    link.href = URL.createObjectURL(blob)
    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  },
  // 判断返回的会话类型是否是后台的数据类型
  isBackendResponse (res) {
    return this.isObject(res) &&
      res.hasOwnProperty('code') &&
      res.hasOwnProperty('data') &&
      res.hasOwnProperty('message')
  },
  // 判断返回的会话类型是否是axios的数据类型
  // await axios({}) 类型的请求会返回这个数据类型
  isAxiosResponse (res) {
    return this.isObject(res) &&
      res.hasOwnProperty('data') &&
      res.hasOwnProperty('status') &&
      res.hasOwnProperty('headers')
  },
  /**
   * 省略多余字符
   * @param {String|Number} text
   * @param {Number} len
   * @return {String} '省略字符x...'
   * @template ellipsisSentence('顶顶顶顶', 3) => '顶顶顶...'
   */
  ellipsisSentence (text = '', len = 10) {
    if (!text) return ''
    let sum = 0
    let res = ''
    // 获取当前文档中，一个默认中文字的宽度
    const defaultWidth = this.countStringSize('中').width
    const limitWidth = defaultWidth * len
    text.split('').forEach((word) => {
      const awidth = this.countStringSize(word).width
      if (sum + awidth <= limitWidth + (defaultWidth / 3)) {
        res += word
        sum += awidth
      }
    })

    if (res === text) {
      return res
    } else {
      return this.appandEllipsis(res)
    }
  },
  /**
   * 强制把语句换行
   * @param {String|Number} sentence
   * @param {Number} len
   * @param {Number} line 如果设置line，超过line的会被省略
   * @return {Array}
   * @template breakSentence('顶顶顶顶顶', 2) => ['顶顶', '顶顶', '顶']
   * @template breakSentence('顶顶顶顶顶', 2, 2) => ['顶顶', '顶...']
   */
  breakSentence (sentence = '', len = 10, line) {
    if (!sentence) return []
    let res = []
    const defaultWidth = this.countStringSize('中').width
    const lineWidthLimit = defaultWidth * len
    let loopLineWidth = 0
    let loopLineIndex = 0
    res[loopLineIndex] = ''
    for (let i = 0; i < sentence.length; i++) {
      const word = sentence[i]
      const wordWidth = this.countStringSize(word).width
      loopLineWidth += wordWidth
      if (isNeedBreak(loopLineWidth)) {
        loopLineWidth = wordWidth
        loopLineIndex += 1
        res[loopLineIndex] = word
      } else {
        res[loopLineIndex] += word
      }
    }

    if (line) {
      const limits = cutLimitLine(res, line)
      if (res.length > limits.length) {
        res = limits
        res[line - 1] = this.appandEllipsis(res[line - 1])
      }
    }

    return res

    function cutLimitLine (src, line) {
      const limit = new Array(line)
      src.forEach((item, index) => limit.fill(item, index, index + 1))
      return limit
    }

    function isNeedBreak (loopLineWidth) {
      const aWordFiff = defaultWidth * (2 / 3)
      return loopLineWidth >= lineWidthLimit + aWordFiff
    }
  },

  appandEllipsis (text) {
    let cutIndex = 1

    // '...' 一般占用（1个中文字符） 或 （2个英文字符）
    const limitCutSize = this.countStringSize('中').width

    countLength.call(this, limitCutSize)

    cutIndex = cutIndex >= text.length ? text.length - 1 : (text.length - cutIndex)

    return text.substring(0, cutIndex || 1) + '...'

    function countLength (limitCutSize) {
      let willCutWord = text.substring(text.length - cutIndex, text.length)
      let willCutSize = this.countStringSize(willCutWord).width
      if (willCutSize < limitCutSize) {
        if (cutIndex < text.length) {
          cutIndex = cutIndex + 1
          return countLength.call(this, limitCutSize)
        }
      }
    }
  },
  /**
   * 获取字符的尺寸, 支持多个字符
   * @param {String|Number} words
   * @return {Object} {width: x, height: y}
  */
  countStringSize (words) {
    if (!this.isString(words) && !this.isNumber(words)) return { width: 0, height: 0 }
    let sizeBox = document.getElementById('__CountStringSizeBox__')
    if (!sizeBox) {
      sizeBox = document.createElement('button')
      sizeBox.style.padding = 0
      sizeBox.style.margin = 0
      sizeBox.style.border = 0
      sizeBox.style.position = 'absolute'
      sizeBox.style.left = -200
      sizeBox.style.top = -200
      sizeBox.id = '__CountStringSizeBox__'
      document.body.appendChild(sizeBox)
    }
    sizeBox.innerHTML = words.replace(/ /g, '&nbsp;')
    return { width: sizeBox.offsetWidth, height: sizeBox.offsetHeight }
  },
  isJSONString (src) {
    if (Object.prototype.toString.call(src) === '[object String]') {
      const firstChar = src[0]
      const lastChar = src[src.length - 1]
      if ((firstChar === '[' && lastChar === ']') || (firstChar === '{' && lastChar === '}')) {
        return true
      }
    }
    return false
  },
  isString (src) {
    return Object.prototype.toString.call(src) === '[object String]'
  },
  isFunction (src) {
    return Object.prototype.toString.call(src) === '[object Function]'
  },
  isNumber (src) {
    return Object.prototype.toString.call(src) === '[object Number]'
  },
  isObject (src) {
    return Object.prototype.toString.call(src) === '[object Object]'
  },
  isBlob (src) {
    return Object.prototype.toString.call(src) === '[object Blob]'
  },
  isEmptyObject (src) {
    return Object.prototype.toString.call(src) === '[object Object]' && isEmpty.call(this, src)
    function isEmpty (src) {
      const res = { empty: true }
      objPropsIteration.apply(this, [src, res])
      return res.empty
    }
    function objPropsIteration (src, res) {
      if (this.isObject(src)) {
        return Object.keys(src).forEach((key) => {
          return objPropsIteration.apply(this, [src[key], res])
        })
      }
      if (this.isArray(src)) {
        return src.forEach((item) => {
          return objPropsIteration.apply(this, [item, res])
        })
      }
      // 只要有一个属性有值，就判断不为空
      if (this.isValuable(src)) {
        res.empty = false
      }
    }
  },
  isArray (src) {
    return Object.prototype.toString.call(src) === '[object Array]'
  },
  isEmptyArray (src) {
    return Object.prototype.toString.call(src) === '[object Array]' && src.length === 0
  },
  isEmpty (src) {
    return this.isNone(src) || this.isEmptyArray(src) || this.isEmptyObject(src)
  },
  isNull (src) {
    return Object.prototype.toString.call(src) === '[object Null]'
  },
  isUndefined (src) {
    return Object.prototype.toString.call(src) === '[object Undefined]'
  },
  isNone (src) {
    return this.isUndefined(src) || this.isNull(src) || src === ''
  },
  isValuable (src) {
    return !this.isUndefined(src) && !this.isNull(src) && src !== ''
  },
  isMoment (src) {
    return this.isObject(src) && (src instanceof moment)
  },
  isDateString (src) {
    return this.isString(src) && this.isMoment(moment(src))
  },
  toString (src) {
    return Object.prototype.toString.call(src)
  },
  clone (srcobject, attrName, value) {
    const newobject = cloneDeep(srcobject)
    if (utils.isValuable(attrName) && utils.isValuable(value)) {
      newobject[attrName] = value
    }
    return newobject
    // let newobject = null
    // if (this.isArray(srcobject)) {
    //   newobject = []
    //   objPropsIteration.apply(this, [srcobject, newobject])
    //   // 数组类型，第二个参数必须是数字
    //   if (this.isNumber(attrName)) {
    //     const index = attrName
    //     newobject[index] = value
    //   }
    // }
    // if (this.isObject(srcobject)) {
    //   newobject = Object.create(srcobject)
    //   objPropsIteration.apply(this, [srcobject, newobject])
    //   // 对象类型，第二个参数必须是有效的字符串
    //   if (this.isValuable(attrName) && this.isString(attrName)) {
    //     newobject[attrName] = value
    //   }
    // }

    // function objPropsIteration () {
    //   const isTop = arguments.length === 2
    //   const [src, res, pkey] = arguments
    //   if (this.isObject(src)) {
    //     if (!isTop) res[pkey] = Object.create(src)
    //     return Object.keys(src).forEach((ckey) => {
    //       return objPropsIteration.apply(this, [src[ckey], isTop ? res : res[pkey], ckey])
    //     })
    //   }
    //   if (this.isArray(src)) {
    //     if (!isTop) res[pkey] = []
    //     return src.forEach((item, index) => {
    //       return objPropsIteration.apply(this, [item, isTop ? res : res[pkey], index])
    //     })
    //   }
    //   res[pkey] = src
    // }

    // return newobject || srcobject
  },
  /**
   * 合并(对象|数组)
   * @param {Object|Array} a
   * @param {Object|Array} b
   * @returns {Object|Array}
   * @template merge({ a: 1 }, { b: 1 }) => { a: 1, b: 1 }
   * @template merge({ a: 1 }, { a: 2 }) => { a: 2 }
   * @template merge([{ a: 1 }], [{ a: 2 }]) => [{ a: 1 }, { a: 2 }]
   */
  merge (a, b) {
    if (utils.toString(a) !== utils.toString(b)) {
      return new Error(`utils.merge => 出现不支持的合并类型!`)
    }
    return merge(a, b)
    // let res = null
    // if (this.isArray(a) && this.isArray(b)) {
    //   res = []
    //   arrItemsIteration.call(this, a, b, res)
    //   return res
    // }
    // if (this.isObject(a) && this.isObject(b)) {
    //   res = Object.create(a)
    //   objPropsIteration.call(this, a, b, res)
    //   return res
    // }
    // return new Error(`utils.merge => 出现不支持的合并类型!`)

    // function objPropsIteration (aObj, bObj, res) {
    //   if (this.isObject(aObj) && this.isObject(bObj)) {
    //     const allKeys = Object.keys(aObj).concat(Object.keys(bObj))
    //     if (allKeys.length) {
    //       allKeys.forEach((key) => {
    //         const av = aObj[key]
    //         const bv = bObj[key]
    //         if (av && bv) {
    //           if (this.isArray(av) && this.isArray(bv)) {
    //             res[key] = []
    //             return arrItemsIteration.call(this, av, bv, res[key])
    //           }
    //           if (this.isObject(av) && this.isObject(bv)) {
    //             res[key] = Object.create(av)
    //             return objPropsIteration.call(this, av, bv, res[key])
    //           }
    //           // 如果相同属性，相同层级，那么只取 b 对象的值
    //           res[key] = bv
    //         } else {
    //           res[key] = av || bv
    //         }
    //       })
    //     }
    //   }
    //   if (this.isArray(aObj) && this.isArray(bObj)) {
    //     arrItemsIteration.call(this, aObj, bObj, res)
    //   }
    // }
    // function arrItemsIteration (aObj, bObj, res) {
    //   const all = aObj.concat(bObj)
    //   all.forEach((item) => {
    //     res.push(item)
    //   })
    // }
    // 数组内部元素合并逻辑，暂时不需要这种合并模式
    // function arrItemsIteration_abandon (aObj, bObj, res) {
    //   const len = aObj.length > bObj.length ? aObj.length : bObj.length
    //   for (let i = 0; i < len; i++) {
    //     const aItem = aObj[i]
    //     const bItem = bObj[i]
    //     if (this.isArray(aItem) && this.isArray(bItem)) {
    //       res[i] = []
    //       arrItemsIteration.call(this, aItem, bItem, res[i])
    //     }
    //     if (this.isObject(aItem) && this.isObject(bItem)) {
    //       res[i] = {}
    //       objPropsIteration.call(this, aItem, bItem, res[i])
    //     }
    //     if (Object.prototype.toString.call(aItem) !== Object.prototype.toString.call(bItem)) {
    //       res[i] = bItem || aItem
    //     }
    //   }
    // }
  },
  /** 拼装 DepartmentSelectPlus 的输入项
   * @params keys => 'xxx,xxx'
   * @params names => 'xxx,xxx'
   * @return [{label: '', key: ''},{label: '', key: ''}]
   */
  spillOptionItems (keys, names) {
    const optionItems = []
    if (keys && names) {
      const namesList = names.split(',')
      keys.split(',').forEach((item, index) => {
        optionItems.push({
          label: `${namesList[index]}`,
          key: JSON.stringify({ key: item, label: namesList[index] })
        })
      })
    }
    return optionItems
  },
  /** 拆分 DepartmentSelectPlus 的输入项
   * @params list => [{label: '', key: ''},{label: '', key: ''}]
   * @return ['num1, num2', 'name1, name2']
   */
  splitOptionItems (list) {
    if (this.isEmpty(list)) {
      return ['', '']
    }
    const listTemp = list.map(item => {
      return JSON.parse(item.key)
    })

    return [listTemp.map(item => {
      return item.key
    }).join(','), listTemp.map(item => {
      return item.label
    }).join(',')]
  },
  bindDefaultValueForComponent (dataSource, formItems) {
    formItems.forEach((item) => {
      const componentName = item.component ? (item.component.name ? item.component.name : item.component) : ''
      switch (componentName) {
        case 'UserSelect':
          if (item.paramKeys && dataSource[item.paramKeys[0]] && dataSource[item.paramKeys[1]]) {
            item.value = this.parseUser(dataSource[item.paramKeys[0]], dataSource[item.paramKeys[1]])
          } else {
            item.value = dataSource[item.key] || []
          }
          break
        case 'DepartmentSelectPlus':
          if (item.paramKeys && dataSource[item.paramKeys[0]] && dataSource[item.paramKeys[1]]) {
            item.value = this.spillOptionItems(dataSource[item.paramKeys[0]], dataSource[item.paramKeys[1]])
          } else {
            item.value = dataSource[item.key] || []
          }
          break
        case 'ADatePicker':
        case 'ATimePicker':
          if (dataSource[item.key]) {
            item.value = moment(dataSource[item.key])
          }
          break
        case 'RangeDatePicker':
          if (item.paramKeys && dataSource[item.paramKeys[0]] && dataSource[item.paramKeys[1]]) {
            item.value = [moment(dataSource[item.paramKeys[0]]), moment(dataSource[item.paramKeys[1]])]
          } else {
            item.value = [dataSource[item.key] || null, dataSource[item.key] || null]
          }
          break
        case 'ARadioGroup':
          if (dataSource[item.key] !== null && dataSource[item.key] !== undefined && dataSource[item.key] !== '') {
            item.value = `${dataSource[item.key]}` // vue的原因，ARadioGroup绑定的key值都是字符串
          }
          break
        default:
          if (dataSource[item.key]) {
            item.value = dataSource[item.key]
          }
          break
      }
    })
    return formItems
  },
  formatFormValues (formValues, operationItems) {
    const res = JSON.parse(JSON.stringify(formValues))
    operationItems.forEach((item) => {
      const valueItem = this.clone(res[item.key])
      const componentName = item.component ? (item.component.name ? item.component.name : item.component) : ''
      switch (componentName) {
        case 'UserSelect':
          if (item.paramKeys) {
            res[item.paramKeys[0]] = this.splitUser(valueItem)[0]
            res[item.paramKeys[1]] = this.splitUser(valueItem)[1]
          } else {
            // 如果只有一个key，那么只获取code
            res[item.key] = this.splitUser(valueItem)[0]
          }
          break
        case 'DepartmentSelectPlus':
          if (item.paramKeys) {
            res[item.paramKeys[0]] = this.splitOptionItems(valueItem)[0]
            res[item.paramKeys[1]] = this.splitOptionItems(valueItem)[1]
          } else {
            // 如果只有一个key，那么只获取code
            res[item.key] = this.splitOptionItems(valueItem)[0]
          }
          break
        case 'SupplierSelect':
          let supplier = store.state.global.supplierList.filter(supplier => supplier.supplierCode === valueItem)
          supplier = supplier && supplier.length ? supplier[0] : {}
          if (item.paramKeys) {
            res[item.paramKeys[0]] = supplier.supplierCode
            res[item.paramKeys[1]] = supplier.abbreviation
          } else {
            // 如果只有一个key，那么只获取code
            res[item.key] = supplier.supplierCode
          }
          break
      }
      // 单独处理moment类型
      if (valueItem instanceof moment) {
        res[item.key] = moment(valueItem).format('YYYY-MM-DD')
      }
      // 裁剪掉多余的key，不过要确保 item.key 不在 item.paramKeys 中
      // if (item.paramKeys && item.key !== item.paramKeys[0] && item.key !== item.paramKeys[1]) {
      //   delete res[item.key]
      // }
    })
    return res
  },
  permissionQueryByRole (src) {
    const pMap = {
      SUPPLIER: '1'
    }
    const res = []
    let role = pMap[store.state.global.userRole.type]
    role = role || '0'
    src.forEach((item) => {
      if (item.permission) {
        if (item.permission.includes(role)) {
          res.push(item)
        }
      } else {
        res.push(item)
      }
    })
    return res
  },
  encodeFileName (src) {
    let prepath = ''
    let fileName = src
    // 需要单独截出文件名，做一次encode，避免 # 和 ？这样的文件名导致url失效
    if (src && src.indexOf('/') > -1) {
      const ps = src.split('/')
      fileName = ps.pop()
      prepath = ps.join('/')
    }
    return `${prepath}/${window.encodeURIComponent(fileName)}`
  },
  getFormErrorMessage (error = {}) {
    const field = Object.keys(error)[0] || ''
    const erObj = error[field].errors ? error[field].errors[0] : {}
    return erObj.message || '请先完成必填项！'
  },
  /**
   * 从证件号码获取年龄
   * @param {Number|String} no
   * @returns {Number}
   */
  countAgeFromIDNumber (no) {
    const birth = this.getBirthFromIDNumber(no)
    if (!birth) return ''
    return new Date().getFullYear() - new Date(birth).getFullYear()
  },
  /**
   * 从证件号码获取生日
   * @param {Number|String} no
   * @returns {String}
   */
  getBirthFromIDNumber (no) {
    if (!no) return ''
    // 15位 1代，18位 2代
    const t1 = /^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}$/
    const t2 = /^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/
    if (!t1.test(no) && !t2.test(no)) return ''
    const year = (no + '').substring(6, 10)
    const month = (no + '').substring(10, 12)
    const date = (no + '').substring(12, 14)
    return `${year}-${month}-${date}`
  },
  readBlobAsText (blob) {
    return new Promise((resolve, reject) => {
      if (this.isBlob(blob)) {
        const r = new FileReader()
        let res = ''
        r.onload = function (event) {
          const { currentTarget: { result } } = event
          res += result || ''
        }
        r.onloadend = function (e) {
          resolve(res)
        }
        r.readAsText(blob)
      } else {
        resolve(blob)
      }
    })
  },
  /**
   * 异步查询html元素，10秒钟内查找不到会抛出错误
   * @param {String} mark 主要是querySelector的参数
   * @param {Number} loopTime 查询次数，1次500ms，默认20次
   * @returns {Promise[Element]}
   * @template await getElementAsync('body') => Element
   * @template await getElementAsync('.class') => Element
   * @template await getElementAsync('#id') => Element
   */
  getElementAsync (mark, loopTime = 20) {
    return new Promise((resolve, reject) => {
      loop(mark, loopTime)
      function loop (_m, _t) {
        const el = document.querySelector(_m)
        if (el) {
          resolve(el)
        } else {
          setTimeout(() => {
            _t = _t - 1
            if (_t > 0) {
              return loop(_m, _t)
            } else {
              return reject(new Error('utils.getElementAsync找不到指定的元素：' + _m))
            }
          }, 500)
        }
      }
    })
  },
  /**
   * 封装一个对象，这个对象可以无视访问边界
   * @param {Object} obj 要封装的对象
   * @param {*} top 给递归用的，正常调用不需要传值
   * @returns {Proxy}
   * @template createFatGetter({ a: { b: { c: 123 } } })
   *                  => Proxy({ a: { b: Proxy(...) }... })
   */
  createFatGetter (obj, top) {
    if (!top) {
      top = defineProps(obj, null, Object.create(null))
      utils.createFatGetter(obj, top)
    }

    Object.keys(obj).forEach((key) => {
      let nextObj = obj[key]
      top[key] = defineProps(nextObj, key, Object.create(null))
      utils.createFatGetter(nextObj, top[key])
      top[key] = createProxy(top[key])
    })

    function defineProps (_obj, _key, _top) {
      _top['_k'] = _key // 绑定 key 值
      if (_key === null) {
        _top['_isTop'] = true // 确认是否是顶层对象
      }
      if (utils.isValuable(_obj)) {
        _top['_v'] = utils.clone(_obj) // 绑定返回值，外部可以通过访问这个来获取真实的值，这种访问不会经过 proxy
        _top['_c'] = !!(Object.keys(_obj).length) // 是否有子项
        _top['_ct'] = Object.prototype.toString.call(_obj) // 子项类型
      }
      return _top
    }

    function createProxy (_obj) {
      return new Proxy(_obj, {
        get (obj, key) {
          // 判断结束符，遇到结束符就直接返回真实值
          if (hasAccessOver(key)) {
            return obj['_v']
          }
          if (hasProp(obj, key)) {
            // 如果有子项"_c"，那么，就需要返回 proxy
            // 如果没有子项，就返回 $end 值
            if (obj['_c']) {
              return obj[key]
            } else {
              return obj['_v']
            }
          } else {
            // 当突破访问边界时，重新构造一个空值的 proxy
            return createProxy({ _v: undefined })
          }
        }
      })

      function hasAccessOver (key) {
        return key === '$end' || /.+(\$)$/.test(key)
      }
    }

    function hasProp (o, k) {
      return Object.prototype.hasOwnProperty.call(o, k)
    }

    // 最后再用proxy封装顶层的top对象
    if (top._isTop) {
      top = createProxy(top)
    }

    return top
  },

  /**
   * 通过字符串的形式，创建一个链式map
   * @param {String} string
   * @param {*} endval 最后一层的赋值，默认为 undefined
   * @returns {Object}
   * @template createChainMap('a.b.c.d') => { a: { b: { c: { d: undefined } } } }
   * @template createChainMap('a.b.c.d', true) => { a: { b: { c: { d: true } } } }
   * @template createChainMap('a.b.c.d', {}) => { a: { b: { c: { d: {} } } } }
   */
  createChainMap (string, endval) {
    if (!utils.isString(string)) return createmap()
    let res = createmap()
    const fields = string.split('.')
    const fieldPath = []
    for (let i = 0; i < fields.length; i++) {
      const field = fields[i]
      fieldPath.push(field)
      setField(res, [...fieldPath], fieldPath.length === fields.length)
    }
    return res

    function setField (res, fieldPath, isEnd) {
      for (let i = 0; i < fieldPath.length;) {
        const field = fieldPath[i]
        if (res[field]) {
          fieldPath.shift()
          setField(res[field], fieldPath, isEnd)
          break
        } else {
          res[field] = isEnd ? endval : createmap()
        }
      }
    }
    function createmap () {
      return Object.create(null)
    }
  }
}

export default utils

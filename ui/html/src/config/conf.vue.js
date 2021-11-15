import Vue from 'vue'
import VueBus from 'vue-bus'
import utils from '@/utils'
import { Modal, Message } from 'ant-design-vue'

// 兼容在 IE11 中，打开本地文件 localStorage 为 undefined 的bug
Vue.localStorage = window.localStorage
Vue.sessionStorage = window.sessionStorage
if (!Vue.localStorage && !Vue.sessionStorage) {
  const map = ['sessionStorage', 'localStorage']
  map.forEach((field) => {
    const storage = Vue[field] = {}
    storage.setItem = (key, val) => {
      if (key !== 'setItem') {
        if (type(val) === 'string') {
          storage[key] = val
        } else {
          storage[key] = JSON.stringify(val)
        }
      }
    }
    storage.getItem = (key) => {
      if (key !== 'getItem') {
        return storage[key]
      }
    }
    storage.removeItem = (key) => {
      if (key !== 'removeItem') {
        delete storage[key]
      }
    }
  })
}

Vue.config.productionTip = false
Vue.use(VueBus)

Vue.prototype.$message = Message
Vue.prototype.$modal = Modal
Vue.prototype.$utils = utils

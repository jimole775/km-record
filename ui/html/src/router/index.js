import Vue from 'vue'
import Router from 'vue-router'
import { setToken, setOMSJump } from '@/utils/auth'
import qs from 'qs'
import Store from '@/store/index'
import base64 from '@/utils/base64'
// import examplesRoutes from '@/helper/examples/router/index.js'
Vue.use(Router)
const context = require.context('./modules', true, /(\.js)$/)
const routerProxy = {
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/home/Home.vue')
    }
  ]
}
context.keys().forEach((item) => {
  routerProxy.routes = routerProxy.routes.concat(context(item).default || context(item))
})

// if (process.env.NODE_ENV === 'development') {
//   routerProxy.routes = routerProxy.routes.concat(examplesRoutes)
// }
const router = new Router(routerProxy)
router.beforeEach((to, from, next) => {
  if (to.query.omsjump) {
    // 处理并缓存外部链接的跳转信息
    const omsjump = to.query.omsjump
    let url = to.fullPath.split('?')[0]
    let splitParmas = to.fullPath.split('?')[1]
    let parmasObj = qs.parse(splitParmas)
    delete parmasObj.omsjump
    let path = url + '?' + qs.stringify(parmasObj)
    // mo跳转数据需要用base64解码
    setOMSJump(base64.decode(omsjump))
    next(path)
  }
  if (to.query.token) {
    // 处理并缓存token
    const token = to.query.token
    let url = to.fullPath.split('?')[0]
    let splitParmas = to.fullPath.split('?')[1]
    let parmasObj = qs.parse(splitParmas)
    delete parmasObj.token
    let path = url + '?' + qs.stringify(parmasObj)
    setToken(token)
    next(path)
  } else {
    // 新增缓存用户信息
    if (!Store.state.global.user) {
      Store.dispatch('loadUser').then(() => {
        next()
      })
    } else {
      next()
    }
  }
})

export default router

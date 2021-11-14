import axios from 'axios'
import { setToken, getToken } from '@/utils/auth'
import utils from '@/utils'
import qs from 'qs'

// create an axios instance
const http = axios.create({
  // baseURL: '/api/', // url = base url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 30000 // request timeout
})

// request interceptor
http.interceptors.request.use(
  config => {
    // do something before request is sent
    let to = qs.parse(location.search.split('?')[1])
    /** 避免出现两个token的情况 */
    if (to.token && to.token.length) {
      if (utils.isString(to.token)) {
        setToken(to.token)
      }
      if (utils.isArray(to.token)) {
        setToken(to.token[0])
      }
    }
    config.headers['x-token'] = getToken()
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// response interceptor
http.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    try {
      const res = 'status' in response ? response.data : response
      if (res.code === 403) {
        let goUrl = document.location.href
        if (goUrl.charAt(goUrl.length - 1) === '/') {
          goUrl.substring(0, goUrl.length - 1)
        }
        let url = res.data + goUrl
        location.href = url
      }
      return res
    } catch (e) {
      return response
    }
  },
  error => {
    return Promise.reject(error)
  }
)

export default http

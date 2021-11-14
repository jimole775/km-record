/**
 * 基础模块
 */
import http from '@/utils/http'
// const base = '/api'
const base = '/mock'
export default {
  getuser () {
    return http.get(`${base}/home/user`)
  },
  getPermissionMenu () {
    return http.get(`${base}/home/menu`)
  },
  getuserpool () {
    return http.get(`${base}/home/user-pool`)
  }
}

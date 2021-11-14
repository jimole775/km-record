import http from '@/utils/http'
// const base = '/api'
const base = '/mock'
export default {
  postDictList () {
    return http.get(`${base}/examples/s-table/1`)
  }
}

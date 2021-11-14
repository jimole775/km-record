import http from '@/utils/http'
// const base = '/api'
const base = '/mock'
export default {
  examplesstable1 () {
    return http.get(`${base}/examples/s-table/1`)
  },
  examplesstable2 (params) {
    return http.post(`${base}/examples/s-table/2`, params)
  },
  examplesstable3 (params) {
    return http.post(`${base}/examples/s-table/3`, params)
  },
  examplesstable4 (params) {
    return http.post(`${base}/examples/s-table/4`, params)
  },
  examplesstable5 (params) {
    return http.post(`${base}/examples/s-table/5`, params)
  }
}

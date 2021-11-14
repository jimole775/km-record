import { Random } from 'mockjs'
export default {
  code: 200,
  message: 'success',
  'data|50': [{
    'name': '@cname',
    'age': '@int(22, 60)',
    'money': '@int(1000, 20000)',
    'level': '@int(10, 19)',
    'start': function () {
      const year = Random.integer(2010, 2019)
      const month = Random.integer(1, 12)
      const day = Random.integer(1, 28)
      return `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day}`
    },
    'end': function () {
      const year = Random.integer(2020, 2021)
      const month = Random.integer(1, 12)
      const day = Random.integer(1, 28)
      return `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day}`
    }
  }]
}

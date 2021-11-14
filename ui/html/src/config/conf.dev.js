if (process.env.NODE_ENV === 'development') {
  require('@/mock') // mock data开关
  require('@/plugins/highlight')
}

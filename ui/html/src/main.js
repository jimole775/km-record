// import '@babel/polyfill'
import './config/load.styles'
import './config/load.modules'
import './config/conf.dev'
import './config/conf.vue'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './config/load.modules'
import './config/load.styles'
import './config/conf.dev'
import './config/conf.vue'

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

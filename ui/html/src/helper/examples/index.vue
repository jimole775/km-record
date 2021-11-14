<template>
  <Layout>
    <div class="base">
      <router-view keep-alive />
    </div>
  </Layout>
</template>
<script>
import Vue from 'vue'
import { mapActions } from 'vuex'
import Layout from './common/layout'
import Panel from './common/panel'
export default {
  components: {
    Layout
  },
  created () {
    Vue.use(Panel)
    Vue.component(Panel.name, Panel)
    this.loadUser()
    this.loadDictList()
  },
  methods: {
    ...mapActions(['loadDictList', 'loadUser'])
  }
}
</script>

<style lang="less" scoped>
.base {
  background: #fff;
  padding: 1rem;
}
</style>

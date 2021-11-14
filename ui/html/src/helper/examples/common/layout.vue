<template>
  <a-layout id="layout-custom">
    <a-layout-sider
      :trigger="null"
      class="oms-sider"
      width="190"
    >
      <div class="logo-text pd-x" style="max-height:50px;">
        <div class="logo-image">
          <span class="logo-desc">组件样例</span>
          &nbsp;&nbsp;
          <router-link to="/">
            <a-tooltip title="退回主页">
              <a-icon type="left-circle" />
            </a-tooltip>
          </router-link>
        </div>
      </div>
      <Menu />
    </a-layout-sider>
    <a-layout>
      <a-layout-content class="content-box">
        <slot />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script>
import Menu from './menu'
export default {
  name: 'Layout',
  components: {
    Menu
  },
  data () {
    return {
    }
  },
  computed: {
    user () {
      return this.$store.state.global.user
    }
  },
  created () {
  },
  methods: {
  }
}
</script>
<style lang="less">

.ant-layout {
  height: 100%;
  min-width:1180px;
}

.oms-sider {
  background: #FFFFFF!important;
  overflow: hidden;
}

.content-box {
  padding: 2rem;
  border-left: 1px solid #e8e8e8;
  background: #FFFFFF;
}

</style>

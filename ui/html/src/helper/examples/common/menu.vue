<template>
  <a-menu
    v-if="menus.length"
    theme="light"
    mode="inline"
    :class="['menu']"
  >
    <template v-for="item in menus">
      <a-menu-item v-if="!item.children" :key="item.id">
        <router-link :to="item.path">
          <i v-if="item.icon" :class="['far', item.icon]" />
          <span>{{ item.name }}</span>
        </router-link>
      </a-menu-item>
    </template>
  </a-menu>
</template>

<script>
import routerItems from '@/helper/examples/router/index.js'
export default {
  name: 'Menu',
  computed: {
    menus () {
      const tar = (routerItems && routerItems[0]) || {}
      return tar.children || []
    }
  }
}
</script>

<style lang="less" scoped>
.menu {
  height: calc(100% - 50px);
  overflow-x: hidden;
  overflow-y: auto;
  padding-bottom: 20px;
}

// 菜单栏展开状态时，选中项的背景色
.ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
  background: linear-gradient(90deg, #F4F9F5 0%, #E5FAE9 100%);
}

</style>

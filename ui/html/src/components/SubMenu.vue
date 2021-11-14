<template>
  <a-sub-menu
    class="oms-sub-menu"
    :key="menuInfo.id"
    v-bind="$props"
    v-on="$listeners"
  >
    <span slot="title">
      <i v-if="menuInfo.icon" :class="['far', menuInfo.icon]" />
      <span>{{ menuInfo.title }}</span>
    </span>
    <template v-for="item in menuInfo.children">
      <a-menu-item class="oms-sub-menu-item" v-if="!item.children" :key="item.id">
        <router-link :to="!item.path ? '' : item.path">
          <i v-if="item.icon" :class="['far', item.icon]" />
          <span>{{ item.title }}</span>
        </router-link>
      </a-menu-item>
      <sub-menu v-else :key="item.id" :menu-info="item" />
    </template>
  </a-sub-menu>
</template>
<script>
import { Menu } from 'ant-design-vue'

export default {
  isSubMenu: true,
  props: {
    ...Menu.SubMenu.props,
    menuInfo: {
      type: Object,
      required: true
    }
  }
}

</script>
<style lang="less" scoped>
li.oms-sub-menu {
  li.oms-sub-menu-item {
    background: #F9FAFC;
    margin: 0;
    height: 46px;
    line-height: 46px;
  }
}
// 菜单栏展开状态时，选中项的背景色
.ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
  background: linear-gradient(90deg, #F4F9F5 0%, #E5FAE9 100%);
}

ul.ant-menu-inline-collapsed {
  // 收缩时选中项的背景色
  li.oms-sub-menu.ant-menu-submenu.ant-menu-submenu-vertical.ant-menu-submenu-selected {
    background: @primary-color;
    color: #fff;
    // 收缩时选中项的内容盒子
    div.ant-menu-submenu-title {
      margin: 0;
      // 收缩时选中项的图标
      i.far {
        color: #fff;
      }
    }
  }
}
</style>

<template>
  <a-layout id="layout-custom">
    <a-layout-sider
      :trigger="null"
      collapsible
      collapsed-width="50"
      v-model="collapsed"
      class="oms-sider"
      width="190"
    >
      <div class="logo-text pd-x" style="max-height:50px;">
        <div class="logo-image">
          <span v-show="!collapsed" class="logo-desc">管理系统</span>
        </div>
      </div>
      <SMenu :collapsed="collapsed" />
    </a-layout-sider>
    <a-layout>
      <a-layout-header class="bd-bottom">
        <a-icon
          class="trigger"
          :type="collapsed ? 'menu-unfold' : 'menu-fold'"
          @click="collapsedTriger"
        />
        <div class="pull-right">
          <a-avatar icon="user" class="mr5" :src="user.image" />
          <span class="black" v-text="user.name" />
          (<span style="margin: 0 0.2rem;font-size: 12px;" v-text="user.employeeNumber" />
          <span v-if="user.supplierAbbreation" style="margin: 0 0.2rem;font-size: 12px;" v-text="user.supplierAbbreation" />)
          <!-- <a href="/api/user/logout" class="red">注销</a> -->
          <!-- <a href="javascript:;" @click="logout" class="red" /> -->
        </div>
      </a-layout-header>

      <a-layout-content class="pd">
        <slot />
        <a-layout-footer class="oms-footer" :class="{widthChange:collapsed}">
          <a-row>
            <a-col :span="1">
              <div style="position: relative;">
                <!-- 移出文档流，防止显示/隐藏时造成抖动 -->
                <ExportExcelManager style="position: absolute;top:0;left:0;" />
              </div>
            </a-col>
            <a-col :span="14">
              <span>（样板项目）</span>
            </a-col>
            <a-col :span="9">
              <span>
                <a-tooltip :trigger="'click'">
                  <template slot="title">
                    <div>
                      <p>联系我们</p>
                    </div>
                  </template>
                  <span>@Copyright</span>
                </a-tooltip>
              </span>
            </a-col>
          </a-row>
        </a-layout-footer>
        <!-- <o-sidebar :user-name="user.employeeNumber" app-no="1047" :name="user.name" /> -->
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script>
import SMenu from './SMenu'
import utils from '@/utils'
import api from '@/api'
import ExportExcelManager from '@/components/ExportExcelManager.vue'
let collapsed = false
export default {
  name: 'SLayout',
  components: {
    SMenu,
    ExportExcelManager
  },
  data () {
    return {
      collapsed
    }
  },
  computed: {
    user () {
      return this.$store.state.global.user
    }
  },
  methods: {
    async logout () {
      let res = await api.logout()
      if (res.code === 403) {
        location.href = res.data + document.location.origin
      }
    },
    strToYear (date) {
      return utils.strToYear(date)
    },
    collapsedTriger () {
      collapsed = this.collapsed = !this.collapsed
    }
  }
}
</script>
<style lang="less">

.ant-layout {
  height: 100%;
  min-width:1180px;
}
#layout-custom .trigger {
  font-size: 16px;
  line-height: 50px;
  cursor: pointer;
  transition: color 0.3s;
}

#layout-custom .trigger:hover {
  color: #1890ff;
}

#layout-custom .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}

.logo-text {
  padding: 0!important;
  width: 100%;
  font-size: 16px;
  color: #333333;
  font-weight: bold;
  line-height: 50px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;

  .logo-image {
    width: 85%;
    height: 100%;
    white-space: nowrap;
  }
  .logo-desc {
    color: #2DC84D;
    margin-left: 6px;
    font-size: 14px;
  }
  img {
    // width: 60%;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    margin: 0;
    transition: 1s ease;
    transform: scale(0.9);
  }
}

.oms-footer {
  text-align: right;
  font-size: 14px;
  color: #75767a;
  background-color: #f1f4f8;
  border-top: 1px solid rgba(0,0,0,.1);
  a {
    color: #75767a;
    margin-right: 7px;
    margin-left: 7px;
    font-weight: 700;
  }
}

.oms-sider {
  background: #FFFFFF!important;
  overflow: hidden;
}

.oms-footer.widthChange{
  width: calc(100% - 50px);
}
</style>

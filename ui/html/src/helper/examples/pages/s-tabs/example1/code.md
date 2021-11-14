``` html
<template>
  <div class="moveBox">
    <STabs :ref="'OmsTabsRef'" :tab-proxy="tabProxy" />
    <div v-show="tabProxy.showList">
      <br>
      <a-button type="primary" @click="() => addDetailTab('1', { id: 1 })">申请页1</a-button>
      &nbsp;&nbsp;
      <a-button type="primary" @click="() => addDetailTab('1', { id: 2 })">申请页2</a-button>
      &nbsp;&nbsp;
      <a-button type="primary" @click="() => addDetailTab('2', { id: 1 })">详情页1</a-button>
      &nbsp;&nbsp;
      <a-button type="primary" @click="() => addDetailTab('1', { id: 2 })">详情页2</a-button>
    </div>
    <div v-show="tabProxy.showApply">
      <br>
      <a-button type="primary" @click="() => removePane()">关闭申请页</a-button>
    </div>
    <div v-show="tabProxy.showDetail">
      <br>
      <a-button type="primary" @click="() => removePane()">关闭详情页</a-button>
    </div>
  </div>
</template>
<script>
export default {
  data () {
    return {
      tabProxy: {
        panes: [
          {
            tabName: '建设申请',
            // 由于是多tab的原因，需要由list来明确apply和detail的title
            proxyName: { apply: '建设申请', detail: '建设详情' },
            // 默认都是list类型，apply和detail都是动态新增的，不需要配置
            type: 'list',
            tabId: '0',
            // list类型的tab一般是不允许用户关闭的
            closable: false,
            // 决定page是否显示的标记，同一时间只允许显示一个page
            show: true,
            // 主要是用来控制权限的
            // 1. roles是根据来决定，比如：供应商不可以看到【部门tab】
            // 2. config是根据服务端配置的权限来决定的，比如：一个角色的【部门tab】查看权限被关闭，那么，就需要做出相应的判断
            permission: {
              roles: [],
              config: ''
            }
          }
        ],
        showList: true, // 指示可否显示list类型的page
        showApply: false, // 指示可否显示apply类型的page
        showDetail: false, // 指示可否显示detail类型的page
        activeId: '0', // 标记当前被激活的tabId
        lastListId: '0' // 标记最后一个被点击的list的tabId
      }
    }
  },
  methods: {
    async addDetailTab (typeId, recordData) {
      await this.$refs.OmsTabsRef
      this.$refs.OmsTabsRef.addDetailTab(typeId, recordData)
    },
    async removePane (id) {
      await this.$refs.OmsTabsRef
      this.$refs.OmsTabsRef.removePane(this.tabProxy.activeId)
    }
  }
}
</script>
```

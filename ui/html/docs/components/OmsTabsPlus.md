### 样例
``` vue
<template>
  <STab :ref="'STabRef'" :tab-proxy="tabProxy" />
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
            proxyName: { apply: 'ODC建设申请', detail: 'ODC建设详情' },
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
              config: '....'
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
  }
}
</script>
```

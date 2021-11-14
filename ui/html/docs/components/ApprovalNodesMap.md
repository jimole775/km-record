### 概述
注意这个组件和 <ApprovalStepBar /> 区别，这个组件只是陈列所有审批节点，并不进行节点匹配
### 样例
``` vue
<template>
  <ApprovalNodesMap :api-name="'postpoprojectfindFlowNode'" :params="{ organizationCode }" />
</template>
<script>
import ApprovalNodesMap from '@/components/ApprovalNodesMap'
export default {
  components: {
    ApprovalNodesMap
  },
  data () {
    return {
      organizationCode: ''
    }
  }
}
</script>
```

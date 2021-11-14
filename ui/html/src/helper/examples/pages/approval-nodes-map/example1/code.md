``` html
<template>
  <ApprovalNodesMap api-name="postpoprojectfindFlowNode" :params="{ organizationCode }" />
</template>
<script>
import ApprovalNodesMap from '@/components/ApprovalNodesMap'
export default {
  components: {
    ApprovalNodesMap
  },
  data () {
    return {
      organizationCode: '313171'
    }
  }
}
</script>
```

``` html
<template>
  <ApprovalStepBar :id="dataSource.flowInstanceId" />
</template>
<script>
import ApprovalStepBar from '@/components/ApprovalStepBar'
export default {
  components: {
    ApprovalStepBar
  },
  data () {
    return {
      dataSource: {
        flowInstanceId: 3069
      }
    }
  }
}
</script>
```

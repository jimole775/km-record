### 概述
旧版本的审批走马灯是直接使用a-step写在页面上的
项目包之后，才把这个小模块抽成一个独立模块

### 样例
``` vue
<template>
  <ApprovalStepBar
    :id="flowInstanceId" # 后台需要的标识
    @update="updateCurrentNode" # 通过这个方法，可以获取当前节点的状态，不过，对于父组件来说，这个结果是异步的
  />
</template>
<script>
import ApprovalStepBar from '@/components/ApprovalStepBar'
export default {
  components: {
    ApprovalStepBar
  },
  data () {
    return {
      flowInstanceId: 123 // 这个标识一般由列表页获取
    }
  },
  methods: {
    updateCurrentNode (currentNode) {
      // 获取当前的流程节点
    }
  }
}
</script>
```

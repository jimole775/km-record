<template>
  <Panel :code="code" title="流程节点样例">
    <template slot="example">
      <ApprovalStepBar :id="dataSource.flowInstanceId" />
    </template>
    <template slot="description">
      id是每条审批流程的 <b>流程实例id（flowInstanceId）</b>，而不是数据库的业务id
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import ApprovalStepBar from '@/components/ApprovalStepBar'
export default {
  title: '流程节点样例',
  name: 'Example1',
  components: {
    ApprovalStepBar
  },
  data () {
    return {
      code,
      dataSource: {
        flowInstanceId: 3069
      }
    }
  }
}
</script>

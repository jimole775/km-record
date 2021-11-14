<template>
  <Panel :code="code" title="流程图样例">
    <template slot="example">
      <ApprovalNodesMap api-name="postpoprojectfindFlowNode" :params="{ organizationCode }" />
    </template>
    <template slot="description">
      params 接口的 "organizationCode" 字段是必填项，必须确定是哪个bumen的流程
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import ApprovalNodesMap from '@/components/ApprovalNodesMap'
export default {
  title: '流程图样例',
  name: 'Example1',
  components: {
    ApprovalNodesMap
  },
  data () {
    return {
      code,
      organizationCode: '313xxx'
    }
  }
}
</script>

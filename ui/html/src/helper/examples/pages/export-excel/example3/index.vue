<template>
  <Panel :code="code" title="权限导出">
    <template slot="example">
      <ExportExcel type="permission" api="exportbudgetManagementexportmanagement" />
    </template>
    <template slot="description">
      通常情况下，即使设置了 permission 类型，也需要 api 接口支持有验证接口
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '权限导出',
  name: 'Example3',
  data () {
    return {
      code
    }
  }
}
</script>

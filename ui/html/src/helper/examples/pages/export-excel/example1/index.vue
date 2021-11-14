<template>
  <Panel :code="code" title="简易导出">
    <template slot="example">
      <ExportExcel api="postkeyeventsexport" />
    </template>
    <template slot="description">
      注意'api'接口接收的是'@/api'中的属性名
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '简易导出',
  name: 'Example1',
  data () {
    return {
      code
    }
  }
}
</script>

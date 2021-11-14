<template>
  <Panel :code="code" title="文件下载">
    <template slot="example">
      <DownLoadFile value="xxx/xx/asd.pdf" />
    </template>
    <template slot="description">
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '文件下载',
  name: 'Example1',
  data () {
    return {
      code
    }
  }
}
</script>

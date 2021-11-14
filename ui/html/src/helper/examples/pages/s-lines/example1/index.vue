<template>
  <Panel :code="code" title="行末省略">
    <template slot="example">
      <div class="color">
        <SLines :value="text" />
      </div>
    </template>
    <template slot="description">
      以换行符（\r\n|\r|\n）为标识，进行语句分割
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '行末省略',
  name: 'Example1',
  data () {
    return {
      code,
      text: `
        1. 超过20个字省略超过20个字省略超过20个字省略
        2. 超过20个字省略超过20个字省略超过20个字省略
        3. 遇到换行符，正常换行，而不是空格
      `
    }
  }
}
</script>
<style lang="less" scoped>
  div.color {
    color: #080;
  }
</style>

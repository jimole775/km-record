<template>
  <Panel :code="code" title="行末换行">
    <template slot="example">
      <div class="color">
        <SLines :value="text" :len="20" line-end="break" />
      </div>
    </template>
    <template slot="description">
      强制换行，而不是省略
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '行末换行',
  name: 'Example2',
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

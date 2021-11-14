<template>
  <Panel :code="code" title="换行">
    <template slot="example">
      <div class="color">
        <SLine
          :len="20"
          :rows="3"
          :value="text"
          :line-end="'break'"
        />
      </div>
    </template>
    <template slot="description">
      如果限制<b>换行行数</b>，超出的部分用省略号代替
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '换行',
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

``` html
<template>
  <div class="color">
    <SLine :value="text" />
  </div>
</template>
<script>
export default {
  name: 'Example1',
  data () {
    return {
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

```

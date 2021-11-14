``` html
<template>
  <div class="color">
    <SLines :value="text" :len="20" line-end="break" />
  </div>
</template>
<script>
export default {
  name: 'Example2',
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

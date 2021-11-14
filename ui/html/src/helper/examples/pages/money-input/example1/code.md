``` html
<template>
  <div style="width: 300px">
    <MoneyInput v-model="value" />
    <a-button type="primary" @click="submitEvent">提交</a-button>
  </div>
</template>
<script>
export default {
  data () {
    return {
      value: null
    }
  },
  methods: {
    async submitEvent () {
      this.$modal.success({
        title: '操作结果',
        content: this.value
      })
    }
  }
}
</script>
```

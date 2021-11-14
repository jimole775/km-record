``` html
<template>
  <div>
    <RangeDatePicker v-model="dataSource.range" />
    <a-button type="primary" @click="submitEvent">提交</a-button>
  </div>
</template>
<script>
export default {
  data () {
    return {
      dataSource: {
        range: []
      }
    }
  },
  methods: {
    async submitEvent () {
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify(this.dataSource.range)
      })
    }
  }
}
</script>
```

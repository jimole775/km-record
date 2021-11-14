``` html
<template>
  <div>
    <YearPicker v-model="dataSource.year" />
    <a-button type="primary" @click="submitEvent">提交</a-button>
  </div>
</template>
<script>
export default {
  data () {
    return {
      dataSource: {
        year: ''
      }
    }
  },
  methods: {
    async submitEvent () {
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify(this.dataSource.year)
      })
    }
  }
}
</script>
```

<template>
  <Panel :code="code" title="年度选择">
    <template slot="example">
      <YearPicker v-model="dataSource.year" />
      <br>
      <br>
      <a-button type="primary" @click="submitEvent">提交</a-button>
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '年度选择',
  name: 'Example1',
  data () {
    return {
      code,
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

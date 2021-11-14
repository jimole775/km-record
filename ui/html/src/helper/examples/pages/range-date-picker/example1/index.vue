<template>
  <Panel :code="code" title="范围选择" :description="description">
    <template slot="example">
      <RangeDatePicker v-model="dataSource.range" />
      <br>
      <br>
      <a-button type="primary" @click="submitEvent">提交</a-button>
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import description from './description.md'
export default {
  title: '范围选择',
  name: 'Example1',
  data () {
    return {
      code,
      description,
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

<template>
  <Panel :code="code" title="极值案例">
    <template slot="example">
      <div style="width: 300px">
        <MoneyInput v-model="value" :min="0" :max="10000" />
        <br>
        <br>
        <a-button type="primary" @click="submitEvent">提交</a-button>
      </div>
    </template>
    <template slot="description">
      设置最大最小值
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '极值案例',
  name: 'Example2',
  data () {
    return {
      code,
      value: 20000
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

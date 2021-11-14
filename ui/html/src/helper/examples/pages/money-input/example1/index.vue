<template>
  <Panel :code="code" title="简易案例">
    <template slot="example">
      <div style="width: 300px">
        <MoneyInput v-model="value" />
        <br>
        <br>
        <a-button type="primary" @click="submitEvent">提交</a-button>
      </div>
    </template>
    <template slot="description">
      简易配置
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '简易案例',
  name: 'Example1',
  data () {
    return {
      code,
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

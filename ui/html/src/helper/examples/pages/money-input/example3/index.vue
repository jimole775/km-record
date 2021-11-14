<template>
  <Panel :code="code" title="限定案例" :description="description">
    <template slot="example">
      <div style="width: 300px">
        <MoneyInput
          v-model="value"
          restrict="negative"
          :min="-10000"
          :max="0"
        />
        <br>
        <br>
        <a-button type="primary" @click="submitEvent">提交</a-button>
      </div>
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import description from './description.md'
export default {
  title: '限定案例',
  name: 'Example3',
  data () {
    return {
      code,
      description,
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

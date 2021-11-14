<template>
  <Panel :code="code" title="编辑样例">
    <template slot="example">
      <div>
        <FormItemRender
          ref="FormItemRenderRef"
          :data-source="dataSource"
          :form-items="formItems"
        />
        <a-button type="primary" @click="submitEvent">提交</a-button>
      </div>
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '编辑样例',
  name: 'Example1',
  data () {
    return {
      code,
      dataSource: {
        code: 112233
      },
      formItems: [
        {
          label: '查询编号',
          key: 'code',
          required: true,
          component: 'AInput'
        }
      ]
    }
  },
  methods: {
    async submitEvent () {
      const res = await this.$refs.FormItemRenderRef.getFieldsValue()
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify(res)
      })
    }
  }
}
</script>

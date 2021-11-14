``` html
<template>
  <div>
    <FormItemRender
      ref="FormItemRenderRef"
      :data-source="dataSource"
      :form-items="formItems"
    />
    <a-button type="primary" @click="submitEvent">提交</a-button>
  </div>
</template>
<script>
export default {
  data () {
    return {
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
```
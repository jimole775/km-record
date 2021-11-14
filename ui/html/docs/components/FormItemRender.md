### 样例
``` vue
<template>
  <FormItemRender
    ref="FormItemRenderRef"
    :data-source="dataSource"
    :active-form-items="formItems"
    :before-render="beforeRender"
    :before-submit="beforeSubmit"
  />
  <a-button @click="submitEvent">提交<a-button>
</template>
<script>
import api from '@/api'
export default {
  data () {
    return {
      dataSource: {}, // 一般当作默认值填入表单中
      formItems: [
        {
          layout: {
            span: 12,
            label: 6,
            wrapper: 18
          },
          label: '交付形式',
          show: true, // 字段是否标志
          required: true, // 字段是否必填
          mode: 'edit', // 编辑状态，如果是readonly并且是编辑组件，默认为禁用
          key: 'deliveryTypeCode', // 和后端交互的字段名
          paramKeys: ['deliveryTypeCode', 'deliveryTypeName'],
          props: {
            'value-field': 'itemCode',
            'group-code': 'dg_delivery'
          },
          labelCustomRender (h, formItem, vm) {
            return vnode
          },
          wrapperCustomRender (h, formItem, vm) {
            return vnode
          },
          change (val, formItem, vm) {},
          component: 'DictSelect' // 组件
        }
      ]
    }
  },
  methods: {
    beforeRender (dataSource, formItem, vm) {},
    beforeSubmit (dataSource, formItem, vm) {},
    async submitEvent () {
      const params = await this.$refs.FormItemRenderRef.getFieldsValue() // 获取字段值
      if (params.type === 'success') {
        const res = await api['submit'](params.data)
        if (res.code === 200) {
          this.$modal.success(res.message)
        }
      }
    }
  }
}
</script>
```
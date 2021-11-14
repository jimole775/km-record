### 样例
``` vue
<template>
  <FormItemViewRender
    ref="FormItemViewRenderRef"
    :cloumns="cloumns"
    :data-source="dataSource"
    :before-render="beforeRender"
  />
</template>
<script>
import api from '@/api'
import FormItemViewRender from '@/components/FormItemViewRender'
export default {
  components: {
    FormItemViewRender
  },
  data () {
    return {
      dataSource: {}, // 一般当作默认值填入表单中
      cloumns: [
        {
          layout: {
            span: 12,
            label: 6,
            wrapper: 18
          },
          label: '附件上传',
          key: 'files',
          labelCustomRender (h, formItem, vm) {
            return vnode
          },
          wrapperCustomRender (h, formItem, vm) {
            return vnode
          }
        }
      ]
    }
  },
  methods: {
  }
}
</script>
```
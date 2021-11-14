<template>
  <Panel :code="code" title="关联样例">
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
    <template slot="description">
      通过 show 字段来控制元素的显示，隐藏。控制逻辑来自 v-if 指令。<br>
      但是，需要注意的是：<br>
      如果设置了 required 字段为 true，即使元素被隐藏了，也会进行必填校验。
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '关联样例',
  name: 'Example3',
  data () {
    return {
      code,
      dataSource: {
        switch: 0
      },
      formItems: [
        {
          label: '字段开关',
          key: 'switch',
          wrapperCustomRender (h, formItem, vm) {
            const tar = vm.$$target || {}
            const formItems = tar.formItems || []
            function activeField (val) {
              if (formItem.value === val) return ''
              formItem.value = val
              formItems.forEach((item) => {
                if (item.key === 'field1') {
                  if (val === 1 || val === 0) {
                    item.show = true
                  } else {
                    item.show = false
                  }
                }
                if (item.key === 'field2') {
                  if (val === 2 || val === 0) {
                    item.show = true
                  } else {
                    item.show = false
                  }
                }
              })
              tar.$forceUpdate()
            }
            return (
              <a-select value={formItem.value} onChange={activeField}>
                <a-select-option key={0}>全部</a-select-option>
                <a-select-option key={1}>字段1</a-select-option>
                <a-select-option key={2}>字段2</a-select-option>
              </a-select>
            )
          }
        },
        {
          label: '关联字段1',
          key: 'field1',
          wrapperCustomRender (h, formItem, vm) {
            const tar = vm.$$target || {}
            const formItems = tar.formItems || []
            function activeField (val) {
              formItem.value = val
              formItems.forEach((item) => {
                if (item.key === 'field2') {
                  if (val === 1) {
                    item.show = true
                  } else {
                    item.show = false
                  }
                }
              })
              tar.$forceUpdate()
            }
            return (
              <a-select onChange={activeField}>
                <a-select-option key={1}>是</a-select-option>
                <a-select-option key={0}>否</a-select-option>
              </a-select>
            )
          }
        },
        {
          label: '关联字段2',
          key: 'field2',
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

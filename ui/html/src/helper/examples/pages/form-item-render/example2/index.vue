<template>
  <Panel :code="code" title="只读样例">
    <template slot="example">
      <div>
        <FormItemRender
          :mode="'readonly'"
          :data-source="dataSource"
          :form-items="formItems"
        />
      </div>
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
export default {
  title: '只读样例',
  name: 'Example2',
  data () {
    return {
      code,
      dataSource: {
        code: 112233
      },
      formItems: [
        {
          label: '查询编号',
          key: 'code'
        }
      ]
    }
  }
}
</script>

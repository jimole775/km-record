<template>
  <Panel :code="code" title="极简样例">
    <template slot="example">
      <STable
        :columns="columns"
        :data-api="'examplesstable2'"
        :is-pagination="false"
        :is-selection="false"
      />
    </template>
    <template slot="description">
      只展示列表
    </template>
  </Panel>
</template>
<script>
import STable from '@/components/STable'
import utils from '@/utils'
import code from './code.md'
export default {
  title: '极简样例',
  name: 'Example2',
  components: {
    STable
  },
  data () {
    return {
      code,
      columns: [
        {
          title: '姓名',
          dataIndex: 'name'
        },
        {
          title: '年龄',
          dataIndex: 'age'
        },
        {
          title: '钱财',
          dataIndex: 'money',
          customRender (text) {
            return `$ ${utils.number2money(text)}`
          }
        },
        {
          title: '等级',
          dataIndex: 'level',
          customRender (text) {
            return `lv.${text}`
          }
        },
        {
          title: '开始日期',
          dataIndex: 'start'
        },
        {
          title: '结束日期',
          dataIndex: 'end'
        }
      ]
    }
  }
}
</script>

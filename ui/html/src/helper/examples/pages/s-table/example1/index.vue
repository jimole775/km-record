<template>
  <Panel :code="code" title="常用样例">
    <template slot="example">
      <STable
        :columns="columns"
        :data-api="'examplesstable1'"
      />
    </template>
    <template slot="description">
      最简单配置
    </template>
  </Panel>
</template>
<script>
import STable from '@/components/STable'
import utils from '@/utils'
import code from './code.md'
export default {
  title: '常用样例',
  name: 'Example1',
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

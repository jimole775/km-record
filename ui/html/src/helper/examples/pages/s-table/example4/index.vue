<template>
  <Panel :code="code" title="审批集成案例">
    <template slot="example">
      <STable
        :columns="columns"
        :data-api="'examplesstable4'"
        :export-api="'postworkRuleFlowexport'"
        :close-api="'postworkRuleFlowcloseFlow'"
        :revoke-api="'postworkRuleFlowwithdrawFlow'"
      />
    </template>
    <template slot="description">
      当前样例展示“导出”“撤回”“关闭”，剩下的按钮可查询 <b>STable.md</b> 文档
    </template>
  </Panel>
</template>
<script>
import STable from '@/components/STable'
import utils from '@/utils'
import code from './code.md'
export default {
  title: '审批集成',
  name: 'Example4',
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

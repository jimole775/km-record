<template>
  <Panel :code="code" title="查询样例">
    <template slot="example">
      <STable
        :columns="columns"
        :searchor="searchor"
        :data-api="'examplesstable3'"
      />
    </template>
    <template slot="description">
      "城市"和"工作地点"，属于关联查询<br>
      "工作地点"依赖"城市"的选值
    </template>
  </Panel>
</template>
<script>
import STable from '@/components/STable'
import utils from '@/utils'
import code from './code.md'
export default {
  title: '查询样例',
  name: 'Example3',
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
      ],
      searchor: [
        {
          key: 'name',
          title: '姓名',
          component: 'AInput'
        },
        {
          key: 'age',
          title: '年龄',
          component: 'AInput'
        },
        {
          key: 'money',
          title: '钱财',
          component: 'MoneyInput'
        },
        {
          title: '日期范围',
          keys: ['start', 'end'],
          component: 'RangeDatePicker'
        },
        {
          title: '等级',
          key: 'level',
          props: {
            'group-code': 'dg_tm',
            'value-field': 'itemName'
          },
          component: 'DictSelect'
        }
      ]
    }
  }
}
</script>

<template>
  <Panel :code="code" title="栅格修饰案例">
    <template slot="example">
      <STable
        :columns="columns"
        :data-api="'examplesstable5'"
        :is-pagination="false"
        :is-selection="false"
      />
    </template>
    <template slot="description">
      主要通过赋值回调的形势来修饰栅格<br>
      thead cell => slotsRender(h, vm)<br>
      tbody cell => scopedSlotsRender(h, record, vm)
    </template>
  </Panel>
</template>
<script>
import STable from '@/components/STable'
import utils from '@/utils'
import code from './code.md'
export default {
  title: '栅格修饰',
  name: 'Example5',
  components: {
    STable
  },
  data () {
    return {
      code,
      columns: [
        {
          dataIndex: 'name',
          slots: { title: 'nameTitle' },
          slotsRender (h, vm) {
            return (
              <div>
                <span>姓名&nbsp;</span>
                <a-tooltip title="姓名提示">
                  <a-icon type="question-circle-o" />
                </a-tooltip>
              </div>
            )
          },
          scopedSlots: { customRender: 'name' },
          scopedSlotsRender (h, record, vm) {
            return <a onClick={ () => alert(record['name']) }>{ record['name'] }</a>
          }
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

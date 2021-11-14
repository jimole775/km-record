``` html
<template>
  <STable
    :columns="columns"
    :data-api="'postworkRuleFlowpage'"
    :is-pagination="false"
    :is-selection="false"
  />
</template>
<script>
import STable from '@/components/STable'
export default {
  components: {
    STable
  },
  data () {
    return {
      columns: [
        {
          dataIndex: 'col1',
          slots: { title: 'col1Title' },
          slotsRender (h, vm) {
            return (
              <div>
                <span>col1&nbsp;</span>
                <a-tooltip title="col1提示">
                  <a-icon type="question-circle-o" />
                </a-tooltip>
              </div>
            )
          },
          scopedSlots: { customRender: 'col1' },
          scopedSlotsRender (h, record, vm) {
            return <a onClick={ () => alert(record['col1']) }>{ record['col1'] }</a>
          }
        },
        {
          title: 'col2',
          dataIndex: 'col2'
        },
        {
          title: 'col3',
          dataIndex: 'col3'
        },
        {
          title: 'col4',
          dataIndex: 'col4'
        },
        {
          title: 'col5',
          dataIndex: 'col5'
        },
        {
          title: 'col6',
          dataIndex: 'col6'
        }
      ]
    }
  }
}
</script>
```

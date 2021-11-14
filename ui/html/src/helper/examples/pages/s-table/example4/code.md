``` html
<template>
  <STable
    :columns="columns"
    :data-api="'postworkRuleFlowpage'"
    :export-api="'postworkRuleFlowexport'"
    :close-api="'postworkRuleFlowcloseFlow'"
    :revoke-api="'postworkRuleFlowwithdrawFlow'"
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
          title: 'col1',
          dataIndex: 'col1'
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

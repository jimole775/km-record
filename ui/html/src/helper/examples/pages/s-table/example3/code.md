``` html
<template>
  <STable
    :columns="columns"
    :searchor="searchor"
    :data-api="'ppprojecttmbankpage'"
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
          dataIndex: 'col1',
          permission: [0, 1]
        },
        {
          title: 'col2',
          dataIndex: 'col2',
          permission: [0, 1]
        },
        {
          title: 'col3',
          dataIndex: 'col3',
          permission: [0, 1]
        },
        {
          title: 'col4',
          dataIndex: 'col4',
          permission: [0, 1]
        },
        {
          title: 'col5',
          dataIndex: 'col5',
          permission: [0, 1]
        },
        {
          title: 'col6',
          dataIndex: 'col6',
          permission: [0, 1]
        },
        {
          title: 'col7',
          dataIndex: 'col7',
          permission: [0, 1]
        }
      ],
      searchor: [
        {
          key: 'col1',
          title: 'col1',
          component: 'CitySelect',
          permission: [0, 1]
        },
        {
          key: 'col2',
          title: 'col2',
          dependKey: 'col1', // 依赖 col1 的值
          component: 'WorkplaceSelect',
          permission: [0, 1]
        },
        {
          title: 'col3',
          keys: ['col31', 'col32'],
          component: 'RangeDatePicker',
          permission: [0, 1]
        },
        {
          title: 'col4',
          key: 'col4',
          props: {
            'group-code': 'dg_tm',
            'value-field': 'itemName'
          },
          component: 'DictSelect',
          permission: [0, 1]
        }
      ]
    }
  }
}
</script>
```

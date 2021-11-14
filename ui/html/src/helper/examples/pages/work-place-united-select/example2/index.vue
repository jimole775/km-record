<template>
  <Panel :code="code" title="工作地联选">
    <template slot="example">
      <div>
        <WorkPlaceUnitedSelect
          ref="WorkPlaceUnitedSelectRef"
          layout-direction="v"
          :default-list="dataSource.defaultList"
          :org-code="dataSource.orgCode"
        />
        <br>
        <br>
        <a-button type="primary" @click="submitEvent">提交</a-button>
      </div>
    </template>
    <template slot="description">
      联选组件，纵向展示
    </template>
  </Panel>
</template>
<script>
import WorkPlaceUnitedSelect from '@/components/WorkPlaceUnitedSelect'
import code from './code.md'
export default {
  title: '工作地选择',
  name: 'Example2',
  components: {
    WorkPlaceUnitedSelect
  },
  data () {
    return {
      code,
      dataSource: {
        orgCode: '123',
        defaultList: [{
          region: '',
          workPlace: '',
          deliveryType: ''
        }]
      }
    }
  },
  methods: {
    async submitEvent () {
      const res = this.$refs.WorkPlaceUnitedSelectRef.getWorkPlaceList()
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify(res)
      })
    }
  }
}
</script>

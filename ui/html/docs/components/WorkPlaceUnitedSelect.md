### 概述
关联选择组件，分别是 城市，工作地，交付形式 三个关联选框

### 样例
``` vue
<template>
  <WorkPlaceUnitedSelect ref="WorkPlaceUnitedSelectRef" :default-list="workPlaceList" :org-code="orgCode" />
  <a-button @click="submit">提交</a-button>
</template>
<script>
import WorkPlaceUnitedSelect from '@/components/WorkPlaceUnitedSelect'
export default {
  components: {
    WorkPlaceUnitedSelect
  },
  data () {
    return {
      orgCode: 'xxx', // 需要给与部门code
      workPlaceList: [{ // 字段是写死的
        region: '',
        workPlace: '',
        deliveryType: ''
      }]
    }
  },
  methods: {
    submit () {
      const workPlaceList/** 返回的数据结构和this.workPlaceList一致 */ = this.$refs.WorkPlaceUnitedSelectRef.getWorkPlaceList()
      if (!workPlaceList) return false
    }
  }
}
</script>
```

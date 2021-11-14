### 概述
字典
### 样例
``` vue
<template>
  <DictSelect
    mode="multiple" /** default | multiple */
    group-code="guide_read_role"
    value-field="itemCode"
    v-model="param.dict"
    @change="dictChange"
  />
</template>
<script>
export default {
  data () {
    return {
      param: {
        dict: '' | []
      }
    }
  },
  methods: {
    dictChange (val, option) {
      // todo
    }
  }
}
</script>
```

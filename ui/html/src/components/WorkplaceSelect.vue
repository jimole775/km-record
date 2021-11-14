
<template>
  <a-select
    v-model="value"
    :allow-clear="true"
    :placeholder="placeholder"
    @change="handleChange(value)"
  >
    <a-select-option v-for="item in workPlaceOption" :key="item.workingPlace">
      {{ item.workingPlace }}
    </a-select-option>
  </a-select>
</template>

<script>
import api from '@/api'
export default {
  name: 'WorkplaceSelect',
  props: {
    disabled: {
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: '请选择'
    },
    valueField: {
      type: String,
      default: 'itemName'
    },
    initialValue: {
      type: String,
      default: ''
    },
    mode: {
      type: String,
      default: 'default'
    },
    depend: {
      type: String,
      default: ''
    },
    value: {
      type: String,
      default: ''
    }
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  data () {
    return {
      workPlaceOption: []
    }
  },
  watch: {
    depend: {
      handler (val) {
        this.getWorkingPlace(val)
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    // 动态获取工作地点
    getWorkingPlace (depend) {
      api.getWorkingPlaceByRegion(depend).then(res => {
        if (res.code === 200) {
          this.workPlaceOption = res.data
        }
      })
    },
    handleChange (value) {
      this.$emit('change', value)
    }
  }
}
</script>

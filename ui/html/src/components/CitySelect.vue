
<template>
  <a-select
    v-model="value"
    :allow-clear="true"
    :placeholder="placeholder"
    @change="handleChange(value)"
  >
    <a-select-option v-for="item in areaOption" :key="item[valueField]">
      {{ item.region }}
    </a-select-option>
  </a-select>
</template>

<script>
import api from '@/api'
export default {
  name: 'CitySelect',
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
      default: 'region'
    },
    initialValue: {
      type: String,
      default: ''
    },
    mode: {
      type: String,
      default: 'default'
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
      areaOption: []
    }
  },
  created () {
    this.getAllArea()
  },
  methods: {
    // 获取所有地域
    getAllArea () {
      api.getAllArea().then(res => {
        if (res.code === 200) {
          this.areaOption = res.data
        }
      })
    },
    handleChange (value) {
      this.$emit('change', value)
    }
  }
}
</script>

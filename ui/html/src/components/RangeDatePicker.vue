<template>
  <div>
    <a-range-picker
      allow-clear
      v-model="value"
      :format="$props.format"
      :mode="$props.mode"
      :placeholder="$props.placeholder"
      :default-value="$props.defaultValue"
      @change="slectChange"
      @panelChange="panelChange"
    />
  </div>
</template>

<script>
import utils from '@/utils'
/**
 * 当前组件主要是为了解决：
 * STable直接引用ARangePicker造成的问题
 * =>
 * 当点击查询时，数值框被重置
 */
export default {
  name: 'RangeDatePicker',
  props: {
    value: {
      type: Array,
      default: () => []
    },
    defaultValue: {
      type: Array,
      default: () => []
    },
    mode: {
      type: Array,
      default: () => ['date', 'date']
    },
    format: {
      type: String,
      default: 'YYYY-MM-DD'
    },
    placeholder: {
      type: Array,
      default: () => ['开始日期', '结束日期']
    }
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  data () {
    return {}
  },
  methods: {
    // date 模式会调用这个方法
    slectChange (value, optionVal) {
      // optionVal 是构造给 STable 取值用的
      this.$emit('change', value, optionVal)
    },
    // month 的模式会调用这个方法
    panelChange (value, mode) {
      const optionVal = [utils.moment(value[0]).format(this.$props.format), utils.moment(value[1]).format(this.$props.format)]
      // optionVal 是构造给 STable 取值用的
      this.$emit('change', value, optionVal)
    }
  }
}
</script>

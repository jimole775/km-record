<template>
  <div class="month-picker-input">
    <a-month-picker
      style="width: 50%"
      :placeholder="placeholder[0]"
      v-model="attendanceCycleStart"
      :disabled-date="disabledStartDate"
      @focus="getStartFocus()"
      @openChange="handleStartOpenChange"
      @change="startPanelChange"
    />
    <a-month-picker
      style="width: 50%"
      :placeholder="placeholder[1]"
      v-model="attendanceCycleEnd"
      :open="endOpen"
      :disabled-date="disabledEndDate"
      @focus="getEndFocus()"
      @openChange="handleEndOpenChange"
      @change="endPanelChange"
    />
  </div>
</template>

<script>
import utils from '@/utils'
/**
 * 当前组件主要是为了解决：
 * RangePicker配置mode = "['month', 'month']"时，
 * start和end无法同时选择同一个月份的问题，
 * 当然，升级ant-design-vue版本也可以解决，
 * 不过，新特性造成的不兼容问题或者更令人头疼
 */
export default {
  name: 'RangeMonthPicker',
  props: {
    value: {
      type: Array,
      default: () => []
    },
    defaultValue: {
      type: Array,
      default: () => []
    },
    placeholder: {
      type: Array,
      default: () => ['开始月份', '结束月份']
    }
  },
  watch: {
    endOpen (val, oldVal) {
      if (val) {
        this.getEndFocus()
        this.$forceUpdate()
      }
    },
    value (val) {
      if (!val || !val.length) {
        this.reset()
      }
    }
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  data () {
    return {
      attendanceCycleEnd: null,
      attendanceCycleStart: null,
      endOpen: false,
      endValue: null,
      startValue: null
    }
  },
  methods: {
    reset () {
      this.attendanceCycleEnd = null
      this.attendanceCycleStart = null
      this.endValue = null
      this.startValue = null
    },
    handleEndOpenChange (open) {
      this.endOpen = open
    },
    getEndFocus () {
      if (!this.attendanceCycleStart) {
        this.startValue = null
      } else {
        this.startValue = utils.date2YM(this.attendanceCycleStart)
      }
      this.endValue = null
    },
    disabledStartDate (startValue) {
      const endValue = this.attendanceCycleEnd
      if (!startValue || !endValue) {
        return false
      }
      return startValue.valueOf() > endValue.valueOf()
    },
    disabledEndDate (endValue) {
      const startValue = this.attendanceCycleStart
      if (!endValue || !startValue) {
        return false
      }
      return startValue.valueOf() > endValue.valueOf()
    },
    handleStartOpenChange (open) {
      if (!open) {
        this.endOpen = true
      } else {
        this.getStartFocus()
      }
    },
    getStartFocus () {
      this.startValue = null
      if (!this.attendanceCycleEnd) {
        this.endValue = null
      } else {
        this.endValue = utils.date2YM(this.attendanceCycleEnd)
      }
    },
    startPanelChange (moment, value) {
      this.$emit('change', [moment, this.attendanceCycleEnd], [value, this.endValue])
    },
    endPanelChange (moment, value) {
      this.$emit('change', [this.attendanceCycleStart, moment], [this.startValue, value])
    }
  }
}
</script>

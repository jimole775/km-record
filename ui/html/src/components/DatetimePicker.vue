<template>
  <div class="clearfix">
    <a-date-picker
      v-model="dateVal"
      @change="calcTime"
      :default-value="initialValue"
      :disabled-date="disabledDate"
      class="pull-left"
      style="width:200px;"
    />
    <a-time-picker
      :minute-step="5"
      format="HH:mm"
      @change="calcTime"
      v-model="timeVal"
      :default-value="initialValue"
      class="pull-left"
    />
  </div>
</template>

<script>
import utils from '@/utils'
export default {
  name: 'DatetimePicker',
  data () {
    return {
      dateVal: null,
      timeVal: null,
      defaultDate: null,
      defaultTime: null
    }
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    initialValue: {
      type: Object,
      required: false,
      default: null
    }
  },
  methods: {
    calcTime () {
      if (!this.dateVal || !this.timeVal) {
        return this.$emit('change', null)
      }
      const res = utils.moment(this.dateVal.format('YYYY/MM/DD') + ' ' + this.timeVal.format('HH:mm'))
      this.$emit('change', res, utils.date2YMDHM(res))
    },
    disabledDate (current) {
      let todayTime = utils.moment(new Date(utils.moment().endOf('day')) - (24 * 60 * 60 * 1000))
      return current && current < todayTime
    }
  }
}
</script>

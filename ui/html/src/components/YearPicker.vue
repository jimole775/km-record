<template>
  <a-date-picker
    v-model="year"
    mode="year"
    format="YYYY"
    :allow-clear="allowClear"
    :open="yearPickShow"
    @panelChange="panelChange"
    @openChange="openChange"
  />
</template>
<script>
import utils from '@/utils'
export default {
  name: 'YearPicker',
  props: {
    value: {
      type: String,
      default: null
    },
    allowClear: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      year: null,
      yearPickShow: false
    }
  },
  watch: {
    value: {
      handler (val) {
        const date = new Date()
        let year = val || date.getFullYear()
        let month = date.getMonth() + 1
        let day = date.getDate()
        if (val && /-/.test(val)) {
          year = val.split('-')[0]
        }
        if (val && /\//.test(val)) {
          year = val.split('/')[0]
        }
        this.year = utils.moment(`${year}-${month}-${day}`)
      },
      immediate: true
    }
  },
  methods: {
    panelChange (val) {
      this.year = utils.moment(val)
      this.yearPickShow = false
      this.$emit('input', val ? val.format('YYYY') : '') // 输出结果给this.value
    },
    openChange (val) {
      this.yearPickShow = val
    }
  }
}
</script>
<style lang="less">
</style>

<template>
  <a-select
    label-in-value
    style="width: 100%"
    :mode="mode"
    :value="valueList"
    :show-arrow="false"
    :allow-clear="true"
    :filter-option="false"
    :disabled="disabled"
    :show-search="true"
    :placeholder="placeholder"
    :not-found-content="fetching ? undefined : null"
    @search="fetchUser"
    @change="handleChange"
  >
    <a-spin v-if="fetching" slot="notFoundContent" size="small" />
    <a-select-option v-for="item in optionList" :key="item.key">
      {{ item.label }}
    </a-select-option>
  </a-select>
</template>
<script>
import api from '@/api'
import utils from '@/utils'
export default {
  name: 'UserSelect',
  props: {
    value: {
      type: Array,
      default: () => []
    },
    placeholder: {
      type: String,
      default: '请输入'
    },
    mode: {
      type: String,
      default: 'default'
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data () {
    this.fetchUser = utils.debounce(this.fetchUser, 150)
    this.handleChange = utils.debounce(this.handleChange, 150)
    return {
      valueList: utils.clone(this.value),
      fetching: false,
      lastFetchId: 0,
      optionList: []
    }
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  watch: {
    value: function (val) {
      if (val) {
        this.clearData()
        this.valueList = utils.clone(val)
      }
    }
  },
  methods: {
    clearData () {
      this.optionList.length = 0
    },
    async fetchUser (value) {
      this.lastFetchId += 1
      const fetchId = this.lastFetchId
      this.optionList = []
      this.fetching = true
      // 调用接口api
      let obj = {}
      obj.name = value
      let res = await api.getuserpool(obj)
      if (res.code === 200) {
        if (fetchId !== this.lastFetchId) {
          // for fetch callback order
          return
        }
        const list = res.data ? res.data.list : []
        const data = list.map(item => ({
          label: `${item.userName} ${item.displayName}（${item.workDeptName}）`,
          key: JSON.stringify({ key: item.userName, label: item.displayName })
        }))
        this.optionList = data
        this.fetching = false
      }
    },
    handleChange (value) {
      this.clearData()
      let valueList = []
      if (value instanceof Array) {
        valueList = [...value]
      } else if (!value) {
        valueList = []
      } else {
        valueList = [value]
      }
      this.fetching = false
      this.$emit('change', valueList)
    }
  }
}
</script>

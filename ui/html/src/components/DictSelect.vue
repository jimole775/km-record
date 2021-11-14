<template>
  <a-select
    show-search
    option-filter-prop="children"
    :allow-clear="true"
    :disabled="disabled"
    :placeholder="placeholder"
    :mode="mode"
    :value="value"
    :filter-option="filterOption"
    :default-value="initialValue"
    @change="handleChange"
  >
    <a-select-option key="" v-if="showAll">全部</a-select-option>
    <a-select-option v-for="item in dictList" :key="item[valueField]">{{ item.itemName }}</a-select-option>
  </a-select>
</template>

<script>
export default {
  name: 'DictSelect',
  props: {
    immediate: {
      type: Boolean,
      default: true
    },
    disabled: {
      type: Boolean,
      default: false
    },
    groupName: {
      type: String,
      default: ''
    },
    groupCode: {
      type: String,
      default: ''
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
    showAll: {
      type: Boolean,
      default: false
    },
    value: {
      type: [String, Array]
    }
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  watch: {
    value: {
      handler (val) {
        // 这里的监听主要是为了解决：父组件用js直接给this.$props.value赋值时，change事件无响应的问题
        if (val !== null && val !== undefined && this.immediate) {
          this.$emit('change', val, this.getCheckedItem(val))
        }
      },
      immediate: true,
      deep: true
    }
  },
  computed: {
    dictList () {
      if (!this.groupCode && !this.groupName) {
        throw new Error(this.name + '，请提供groupCode或groupName')
      }
      if (this.groupCode) {
        return this.$store.getters.getDictByGroupCode(this.groupCode)
      }
      return this.$store.getters.getDictByGroupName(this.groupName)
    }
  },
  methods: {
    handleChange (val) {
      this.$emit('change', val, this.getCheckedItem(val))
    },
    getCheckedItem (val) {
      if (this.$props.mode === 'multiple') {
        // 多选类型
        let checkedItems = []
        let multiVals = val || []
        multiVals.forEach((v) => {
          this.dictList.forEach((item) => {
            if (item[this.$props.valueField] === v) {
              checkedItems.push(item)
            }
          })
        })
        return checkedItems
      } else {
        // 单选类型
        let checkedItem = {}
        this.dictList.forEach((item) => {
          if (item[this.$props.valueField] === val) {
            checkedItem = item
          }
        })
        return checkedItem
      }
    },
    filterOption (input, option) {
      return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    }
  }
}
</script>

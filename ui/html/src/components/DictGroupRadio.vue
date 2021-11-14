<template>
  <a-radio-group
    :default-value="initialValue"
    :value="value"
    :disabled="disabled"
    @change="handleChange"
  >
    <a-radio-button v-for="item in dictList" :key="item[valueField]" :value="item[valueField]">{{ item.itemName }}</a-radio-button>
  </a-radio-group>
</template>

<script>
export default {
  name: 'DictGroupRadio',
  props: {
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
    valueField: {
      type: String,
      default: 'itemName'
    },
    initialValue: {
      type: String,
      default: ''
    },
    value: {
      type: String,
      default: ''
    }
  },
  model: {
    prop: 'initialValue',
    event: 'change'
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
    handleChange (e) {
      this.$emit('change', e.target.value)
    }
  }
}
</script>

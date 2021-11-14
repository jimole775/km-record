<template>
  <a-input
    ref="moneyinput"
    v-model="view"
    :disabled="disabled"
    :suffix="suffix"
    @input="(e) => inputting(e)"
  />
</template>

<script>
import utils from '@/utils'
export default {
  name: 'MoneyInput',
  props: {
    value: {
      type: Number
    },
    min: {
      type: Number,
      default: -Infinity
    },
    max: {
      type: Number,
      default: Infinity
    },
    suffix: {
      type: String,
      default: '元'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: '请输入金额'
    },
    restrict: {
      type: String/** negative | positive */,
      default: null
    }
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  data () {
    return {
      view: this.value
    }
  },
  watch: {
    value: {
      handler (val) {
        // 根据value的值，刷新默认视图
        if (utils.isValuable(val)) {
          this.updateView(val)
          this.updateValue(val)
        }
      },
      immediate: true
    }
  },
  methods: {
    inputting (e) {
      let result = utils.isNone(e.target.value) ? '' : e.target.value
      this.updateView(result)
      this.updateValue(result)
    },
    updateView (val) {
      if (!isOnlySign(val)) {
        val = this.querySpecialValue(val) // 过滤 '0-' 这个特殊字符
        val = this.computeInputValue(val) // 获取自然数
        val = this.restrictInPositiveOrNegative(val) // 限定正负结果
        val = this.adjustLimit(val) // 修正预期阈值
        val = this.number2money(val) // 修正预期阈值
      }
      this.view = val
    },
    updateValue (val) {
      if (!isOnlySign(val)) {
        val = this.querySpecialValue(val) // 过滤 '0-' 这个特殊字符
        val = this.computeInputValue(val) // 获取自然数
        val = this.restrictInPositiveOrNegative(val) // 限定正负结果
        val = this.adjustLimit(val) // 修正预期阈值
      } else {
        val = null
      }
      this.$emit('change', val) // 更新v-model
    },
    // 限定“正”或“负”结果
    restrictInPositiveOrNegative (val) {
      if (/^[ |0]$/.test(val)) return val // 防止出现 -1 * 0 = -0
      let result = val
      // 只返回正数
      if (this.restrict === 'positive') {
        result = Math.abs(val)
      }
      // 只返回负数
      if (this.restrict === 'negative') {
        result = -1 * Math.abs(val)
      }
      return result // 返回字符串
    },
    computeInputValue (val) {
      // if (isOnlySign(val)) return val
      let purval = utils.money2number(val)
      let result = ''
      // 处理数型数据
      if (isNum(purval)) {
        result = Number.parseFloat(purval)
      }
      return result
    },
    // number 转 money
    number2money (val) {
      if (isNum(val)) {
        return utils.number2money(val)
      } else {
        return ''
      }
    },
    adjustLimit (val) {
      if (val < this.min) {
        return this.min
      }
      if (val > this.max) {
        return this.max
      }
      return val
    },
    // 如果在前面有数字，并且这个数字是0的情况下，需要清除前面的0
    querySpecialValue (val) {
      if (/0-/.test(val)) {
        return '-'
      } else {
        return val
      }
    }
  }
}

// 判断是否是自然数
function isNum (val) {
  return /^([\+\-]?(\d*\.?\d+|\d+\.?\d*))$/.test(val)
}

// 判断是否只是 正负号
function isOnlySign (val) {
  return /^([\+\-])$/.test(val)
}

</script>

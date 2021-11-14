<template>
  <div class="panel-content border-bottom-1" style="overflow:auto">
    <a-steps :style="{padding: '30px 2%', minWidth: '100%', width: autoWidth}" :current="current">
      <a-step
        v-for="item in stepOption"
        :key="item.nodeCode"
        :data-set="item.nodeCode"
        :style="countStyle(item)"
        :status="matchStatus(item.approvalStatus)"
      >
        <template slot="title">
          <a-tooltip :title="item.nodeName">
            <span>{{ item.nodeName }}</span>
          </a-tooltip>
        </template>
      </a-step>
    </a-steps>
  </div>
</template>
<script>
import api from '@/api'
function countNodeWidth (str) {
  // 40: icon宽度
  // 14：字体大小
  // 16：字体 margin
  // 32：连接线预留长度
  return 40 + str.length * 14 + 16 + 32
}

export default {
  name: 'ApprovalStepBar',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data () {
    return {
      stepOption: []
    }
  },
  watch: {
    id (val) {
      this.fetchData(val)
    },
    current: {
      handler (val) {
        if (val !== undefined && val !== null) {
          const map = {
            0: 'wait',
            1: 'process',
            2: 'finish'
          }
          const currentNode = this.stepOption[val] || {}
          if (map[currentNode.approvalStatus] === 'finish' && val === this.stepOption.length - 1) {
            // 如果当前时最后一个节点，且状态为'finish',就置空审批人数组
            currentNode.approvalAccountList = []
          }
          this.$emit('update', currentNode)
        }
      },
      immediate: true,
      deep: true
    }
  },
  computed: {
    autoWidth () {
      let res = 0
      this.stepOption.forEach((node) => {
        res += countNodeWidth(node.nodeName)
      })
      return res ? res + 'px' : 'auto'
    },
    current () {
      let nodeIndex = null
      for (let index = 0; index < this.stepOption.length; index++) {
        const option = this.stepOption[index]
        // 0：待发起
        // 1：审批中
        // 2：正常结束
        // -1:终止
        if (option.approvalStatus === 1 || option.approvalStatus === -1) {
          nodeIndex = index
          break
        }
      }
      // 如果找不到激活中的节点，默认为end节点
      return nodeIndex === null ? this.stepOption.length - 1 : nodeIndex
    }
  },
  async created () {
    await this.fetchData(this.id)
  },
  methods: {
    countStyle (node) {
      return { minWidth: countNodeWidth(node.nodeName) + 'px' }
    },
    async fetchData (id) {
      const res = await api.ppprojectprocessnodes(id)
      if (res && res instanceof Array) {
        this.stepOption = res
      }
      return Promise.resolve()
    },
    matchStatus (approvalStatus) {
      // approvalStatus ：0：未处理，1：处理中，2：已处理
      const map = {
        0: 'wait',
        1: 'process',
        2: 'finish'
      }
      return map[approvalStatus]
    }
  }
}
</script>
<style lang="less" scoped>
// /deep/.ant-steps-item-title::after {
//   height: 0 !important;
// }
</style>

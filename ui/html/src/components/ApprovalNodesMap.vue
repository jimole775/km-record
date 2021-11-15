<template>
  <div class="panel-content border-bottom-1" style="overflow:auto">
    <a-steps :style="{padding: '30px 2%', minWidth: '100%', width: autoWidth}" :current="current">
      <a-step
        v-for="item in nodes"
        :key="item.nodeCode"
        :title="item.nodeName"
        :status="matchStatus(item.approvalStatus)"
      >
        <template slot="icon">
          <a-tooltip v-if="item.workItemGroupList && item.workItemGroupList.length">
            <template slot="title">
              <span>{{ getHandler(item.workItemGroupList) }}</span>
            </template>
            <span class="node-icon">{{ item.nodeOrder }}</span>
          </a-tooltip>
          <span v-else class="node-icon node-default">{{ item.nodeOrder }}</span>
        </template>
      </a-step>
    </a-steps>
  </div>
</template>
<script>
import api from '@/api'
export default {
  name: 'ApprovalNodesMap',
  props: {
    apiName: {
      type: String,
      required: true
    },
    params: {
      type: Object
    }
  },
  data () {
    return {
      nodes: []
    }
  },
  watch: {
    apiName: {
      handler (val) {
        if (val) this.fetchData()
      },
      deep: true,
      immediate: true
    },
    params: {
      handler (val) {
        if (val) this.fetchData()
      },
      deep: true,
      immediate: true
    },
    current: {
      handler (val) {
        if (val !== undefined && val !== null) {
          const currentNode = this.nodes[val] || {}
          this.$emit('update', currentNode)
        }
      },
      deep: true,
      immediate: true
    }
  },
  computed: {
    autoWidth () {
      let res = 0
      // 40: icon宽度
      // 14：字体大小
      // 16：字体 margin
      // 32：连接线预留长度
      this.nodes.forEach((node) => {
        res += 40 + node.nodeName.length * 14 + 16 + 32
      })
      return res ? res + 'px' : 'auto'
    },
    current () {
      return 0
    }
  },
  methods: {
    async fetchData () {
      const res = await api[this.apiName](this.params)
      debugger
      if (res.code === 200) {
        this.nodes = res.data
      }
      return Promise.resolve()
    },
    matchStatus (approvalStatus) {
      // approvalStatus ：0：未处理，1：处理中，2：已处理
      const map = {
        0: 'wait',
        1: 'process',
        2: 'finish',
        null: 'wait'
      }
      return map[approvalStatus]
    },
    getHandler (workItemGroupList = []) {
      const res = []
      workItemGroupList.forEach((item) => {
        const accs = item.approvalAccountList || []
        res.push(accs.join('，'))
      })
      return res.join('，')
    }
  }
}
</script>
<style lang="less" scoped>
.node-icon {
  cursor: pointer;
  display: block;
  width: 2rem;
  height: 2rem;
  background: @primary-color;
  border-radius: 100%;
  color: #fff;
}
.node-default {
  cursor: default;
}
</style>

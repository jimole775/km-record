<template>
  <div class="moveBox">
    <STabs :ref="'OmsTabsRef'" :tab-proxy="tabProxy" />
    <div v-show="tabProxy.showList">
      <template v-for="c in listComponents">
        <ProjectList
          v-show="c.tabId === tabProxy.activeId"
          :key="c.tabId"
          :apimap="c.apimap"
          :list-config="c.listConfig"
          :ref="'ProjectListRef' + c.tabId"
          :transfer-searchor="transferSearchor"
          :stable-row-key="stableRowKey"
          :apply-anchor-text="applyAnchorText"
          :bridge="bridge"
          :tab-proxy="tabProxy"
          :before-render="beforeRender"
          :before-submit="beforeSubmit"
          @addDetailTab="addDetailTab"
        />
      </template>
    </div>
    <div v-show="tabProxy.showApply">
      <template v-for="c in applyComponents">
        <ProjectApply
          v-show="c.tabId === tabProxy.activeId"
          :key="c.tabId"
          :apimap="c.apimap"
          :apply-config="c.applyConfig"
          :ref="'ProjectApplyRef' + c.tabId"
          :bridge="bridge"
          :tab-proxy="tabProxy"
          :before-render="beforeRender"
          :before-submit="beforeSubmit"
          @close="removePane()"
        />
      </template>
    </div>
    <div v-show="tabProxy.showDetail">
      <template v-for="c in approvalComponents">
        <ProjectApproval
          v-show="c.tabId === tabProxy.activeId"
          :ref="'ProjectApprovalRef' + c.tabId"
          :key="c.tabId"
          :apimap="c.apimap"
          :approval-config="c.approvalConfig"
          :bridge="bridge"
          :tab-proxy="tabProxy"
          :before-render="beforeRender"
          :before-submit="beforeSubmit"
          @close="removePane()"
        />
      </template>
    </div>
  </div>
</template>
<script>
import utils from '@/utils'
import baseMixins from '@/mixins/baseMixins'
import todoMixins from '@/mixins/todoMixins'
import ProjectList from './list'
import ProjectApply from './apply'
import ProjectApproval from './approval'
export default {
  name: 'SApprovallor',
  components: {
    ProjectList,
    ProjectApply,
    ProjectApproval
  },
  mixins: [baseMixins, todoMixins],
  props: {
    applyAnchorText: {
      type: String,
      default: '创建'
    },
    stableRowKey: {
      type: String,
      default: 'id'
    },
    listConfig: {
      type: Object,
      default: () => ({})
    },
    apimap: {
      type: Object,
      default: () => ({})
    },
    applyConfig: {
      type: Object,
      default: () => ({})
    },
    approvalConfig: {
      type: Object,
      default: () => ({})
    },
    panes: {
      type: Array,
      default: () => ([])
    },
    beforeRender: {
      type: Function,
      default: p => p
    },
    beforeSubmit: {
      type: Function,
      default: p => p
    },
    bridge: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      tabProxy: {
        panes: utils.clone(this.panes),
        showList: true,
        showApply: false,
        showDetail: false,
        activeId: '0',
        lastListId: '0'
      },
      listComponents: []
    }
  },
  computed: {
    applyComponents () {
      return this.tabProxy.panes.filter((pane) => {
        const live = /\d_1_.+/.test(pane.tabId)
        if (live) {
          pane.applyConfig = utils.clone(this.activeApplyConfig)
          pane.apimap = utils.clone(this.activeApimap)
        }
        return live
      })
    },
    approvalComponents () {
      return this.tabProxy.panes.filter((pane) => {
        const live = /\d_2_.+/.test(pane.tabId)
        if (live) {
          pane.approvalConfig = utils.clone(this.activeApprovalConfig)
          pane.apimap = utils.clone(this.activeApimap)
        }
        return live
      })
    },
    activeApplyConfig () {
      return this.applyConfig[this.tabProxy.lastListId]
    },
    activeApprovalConfig () {
      return this.approvalConfig[this.tabProxy.lastListId]
    },
    activeApimap () {
      return this.apimap[this.tabProxy.lastListId]
    }
  },
  mounted () {
    // listComponents 不能使用 computed 构建
    // 因为 STable 太过冗余，
    // computed 会导致频繁调用渲染函数，
    // 而频繁调用渲染函数会在切换 tab 时导致卡顿
    this.listComponents = this.tabProxy.panes.filter((pane) => {
      const live = pane.type === 'list'
      const listConfig = this.listConfig[pane.tabId] || {}
      const apimap = this.apimap[pane.tabId] || {}
      if (live) {
        pane.listConfig = utils.clone(listConfig)
        pane.apimap = utils.clone(apimap)
      }
      return live
    })
  },
  methods: {
    async addDetailTab (typeId, recordData) {
      await this.$refs.OmsTabsRef
      this.$refs.OmsTabsRef.addDetailTab(typeId, recordData)
    },
    async removePane () {
      await this.$refs.OmsTabsRef
      this.$refs.OmsTabsRef.removePane(this.tabProxy.activeId)
      this.reload()
    },
    async reload () {
      await this.$refs.ProjectListRef
      this.$refs.ProjectListRef.reload()
    }
  }
}
</script>

<template>
  <a-tabs
    hide-add
    type="editable-card"
    v-model="tabProxy.activeId"
    @edit="tabEditEvent"
    @change="tabChangeEvent"
  >
    <a-tab-pane
      v-for="pane in panesView"
      :key="pane.tabId"
      :tab="pane.tabName"
      :closable="!!pane.closable"
    />
  </a-tabs>
</template>
<script>
import utils from '@/utils'
import { mapActions } from 'vuex'
import baseMixins from '@/mixins/baseMixins'
const panelmodel = {
  tabName: '',
  proxyName: null,
  type: 'apply', // 'list' 'apply' 'detail'
  tabId: '1_1',
  closable: true,
  show: true,
  visible: true,
  lastListId: '',
  recordData: {}
}
export default {
  name: 'STabs',
  props: {
    tabProxy: {
      type: Object,
      default: () => ({})
    }
  },
  mixins: [baseMixins],
  data () {
    return {
      // 用来存储点击过的【list类型】的tabid
      // 用push的方式来存储，取的时候，永远取最后一个
      // 主要的作用就是在用户关闭可编辑的tab时，可回溯到最后一个被浏览的list
      usedListIds: [],
      cachePanesLen: null
    }
  },
  computed: {
    // 主要渲染对象
    panesView () {
      return this.tabProxy.panes.filter(pane => pane.show)
    }
  },
  watch: {
    'tabProxy.panes': {
      handler (panes) {
        // tabProxy.panes 有时候是后端返回的，属于异步获取
        // this.init() 中也会对panes进行更改，所以需要用 currentPanesLen 进行预存
        // 防止死循环
        if (panes && panes.length && panes.length !== this.cachePanesLen) {
          this.init()
          this.cachePanesLen = panes.length
        }
      },
      deep: true,
      immediate: true
    },
    'tabProxy.activeId': {
      handler (tabId) {
        if (tabId) {
          const curPanel = this.getPanelFromTabId(tabId)
          // 如果目标pane时【detail】类型，就需要关联跳转前的【list】的tabid
          // 主要为了防止detail页内用lastListId查询数据时的报错
          if (curPanel.type === 'apply') {
            curPanel.__apply_listTabId__ = this.tabProxy.lastListId
          }
          if (curPanel.type === 'detail') {
            curPanel.__detail_listTabId__ = this.tabProxy.lastListId
          }
          this.activePane(tabId)
          this.showPage(tabId)
        }
      },
      immediate: true
    },
    'tabProxy.lastListId': {
      handler (tabId) {
        if (tabId) {
          this.setLastListTabId(tabId)
          this.$emit('update')
        }
      }
    }
  },
  created () {
    this.init()
  },
  methods: {
    ...mapActions(['loadMenuButtons']),
    async init () {
      // 默认一定要加载按钮权限列表
      await this.getMenuButtons()
      // 根据权限列表裁剪有效的panes
      this.queryPermissionPanes()
      // 直接show activeId
      this.activePane(this.tabProxy.activeId)
      return Promise.resolve()
    },
    async getMenuButtons () {
      const menuButtons = this.$store.state.global.menuButtons || []
      if (menuButtons.length === 0) {
        await this.loadMenuButtons()
      }
      return Promise.resolve()
    },
    queryPermissionPanes () {
      const panes = this.tabProxy.panes || []
      const menuButtons = this.$store.state.global.menuButtons || []
      this.tabProxy.panes = panes.filter(pane => {
        const permission = pane.permission || {}
        // 如果设置了 permission.config，就匹配这个的值
        return permission.config ? menuButtons.includes(permission.config) : pane.show
      })
      // 把默认的 pane.show 全部设为 true
      this.tabProxy.panes.forEach(pane => {
        pane.show = true
      })
      if (this.tabProxy.showList) {
        // 默认展示第一个 show 为 true 的 pane
        this.tabProxy.lastListId = this.tabProxy.activeId = this.tabProxy.panes[0].tabId
      }
    },
    activePane (tabId) {
      // 根据提供的id去获取指定的Panel面板
      const curPanel = this.getPanelFromTabId(tabId)
      // 需要把面板show设置为true
      curPanel.show = true
    },
    negativePane (tabId) {
      const curPanel = this.getPanelFromTabId(tabId)
      curPanel.show = false
    },
    addDetailTab (detailType, recordData) {
      // 根据recordData的id来判断当前是否有重复的panel
      if (this.isUniqueTanpe(recordData)) {
        const newPanel = utils.clone(panelmodel)
        const listPanel = this.getPanelFromTabId(this.getLastListTabId())
        newPanel.type = Number.parseInt(detailType) === 1 ? 'apply' : 'detail'
        newPanel.tabId = this.upRiseTabId(this.getLastEditTabId(listPanel.tabId, detailType))
        newPanel.tabName = getTabName(detailType, listPanel)
        newPanel.lastListId = listPanel.tabId
        newPanel.recordData = recordData
        this.tabProxy.activeId = newPanel.tabId
        this.tabProxy.panes.push(newPanel)
      } else {
        // 如果已经渲染的，就直接切换tab就行，不用新增tab
        return this.changeTabByRecordData(recordData)
      }

      function getTabName (_detailType, _listPanel) {
        const defaultsuffix = Number.parseInt(_detailType) === 1 ? '申请' : '审批'
        if (_listPanel.proxyName) {
          return Number.parseInt(_detailType) === 1 ? _listPanel.proxyName.apply : _listPanel.proxyName.detail
        } else {
          return _listPanel.tabName + defaultsuffix
        }
      }
    },
    isUniqueTanpe (recordData = {}) {
      let isUnique = true
      for (let index = 0; index < this.tabProxy.panes.length; index++) {
        const pane = this.tabProxy.panes[index]
        if (pane.recordData && pane.recordData.id === recordData.id) {
          isUnique = false
          break
        }
      }
      return isUnique
    },
    changeTabByRecordData (recordData = {}) {
      for (let index = 0; index < this.tabProxy.panes.length; index++) {
        const pane = this.tabProxy.panes[index]
        if (pane.recordData && pane.recordData.id === recordData.id) {
          this.tabProxy.activeId = pane.tabId
          break
        }
      }
    },
    // tab切换事件
    tabChangeEvent (tabId) {
      const curPanel = this.getPanelFromTabId(tabId)
      // curPan.type === undefined 属于向前兼容
      if (curPanel.type === 'list' || curPanel.type === undefined) {
        this.setLastListTabId(tabId)
      }
      // 目标tab如果是detail，
      // 需要保持 lastListId 是 list 类型的 tabId
      // 因为，申请和详情页有时候需要根据 list 的 tabId 去匹配一些数据
      if (curPanel.type === 'apply') {
        this.setLastListTabId(curPanel.__apply_listTabId__)
      }
      if (curPanel.type === 'detail') {
        this.setLastListTabId(curPanel.__detail_listTabId__)
      }
    },
    // 往 this.usedListIds 里塞 tabId
    setLastListTabId (tabId) {
      const curPanel = this.getPanelFromTabId(tabId)
      if (curPanel.type === 'list' || curPanel.type === undefined) {
        this.tabProxy.lastListId = tabId
        if (!this.usedListIds) {
          this.usedListIds = []
        }
        this.usedListIds.push(tabId)
        if (this.usedListIds.length > 99) {
          this.usedListIds.shift()
        }
      }
    },
    // 获取 this.usedListIds 的最后一位
    getLastListTabId () {
      if (!this.usedListIds) {
        this.usedListIds = []
      }
      return this.usedListIds[this.usedListIds.length - 1] || '0'
    },
    // 获取"详情页"，"申请页",这种可点击删除的Panel的id
    getLastEditTabId (listId, detailType) {
      // 如果是第一次新增panel，给与默认tabId
      let res = this.spillTabId(listId, detailType, 0)
      for (let i = this.tabProxy.panes.length - 1; i > 0; i--) {
        const pane = this.tabProxy.panes[i]
        if (pane.tabId.length > 1 && this.getDetailTypeFormTabId(pane.tabId) === detailType) {
          res = pane.tabId
          break
        }
      }
      return res
    },
    // tab新增或者删除事件
    tabEditEvent (tabId, action) {
      if (action === 'remove') {
        this.removePane(tabId)
      }
    },
    // 关闭标签页
    // 两种情景触发当前方法：
    // 1. 当前只有用户点击【x】操作
    // 2. 审批完毕时，this.$emit('removePane')进行调用
    removePane (tabId) {
      for (let i = 0; i < this.tabProxy.panes.length; i++) {
        const pane = this.tabProxy.panes[i]
        if (pane.tabId === tabId) {
          this.tabProxy.panes.splice(i, 1)
          break
        }
      }
      // activeId 切换到最后一个 list
      this.tabProxy.activeId = this.getLastListTabId()
      // 这里手动activePane，是为了防止activeId没改变，导致没触发watch方法的情况
      this.activePane(this.tabProxy.activeId)
    },
    getPanelFromTabId (tabId) {
      let correctPanel = this.tabProxy.panes.filter((pan) => pan.tabId === tabId)
      correctPanel = correctPanel && correctPanel.length ? correctPanel[0] : {}
      return correctPanel
    },
    /**
     * 父级html是这样写的:
     * @html # <div v-if="tabProxy.showList">
     * @html #   <List />
     * @html # </div>
     * @html # <div v-if="tabProxy.showApply">
     * @html #   <Apply />
     * @html # </div>
     * @html # <div v-if="tabProxy.showDetail">
     * @html #   <Approval />
     * @html # </div>
     */
    showPage (tabId) {
      this.tabProxy.showList = false
      this.tabProxy.showApply = false
      this.tabProxy.showDetail = false
      if (/_/.test(tabId)) {
        if (this.getDetailTypeFormTabId(tabId) === '1') {
          this.tabProxy.showApply = true
        }
        if (this.getDetailTypeFormTabId(tabId) === '2') {
          this.tabProxy.showDetail = true
        }
      } else {
        this.tabProxy.showList = true
      }
    },
    // tabid 通过这样的逻辑来创建:
    // 'apply': 0_1_0 [列表下标_类型_自增下标]
    // 'detail': 0_2_0 [列表下标_类型_自增下标]
    upRiseTabId (tabId) {
      const listId = this.getListIdFormTabId(tabId)
      const type = this.getDetailTypeFormTabId(tabId)
      const detailId = this.getDetailIdFormTabId(tabId)
      return this.spillTabId(listId, type, detailId + 1)
    },
    spillTabId (listId = '0', type = '1', detailId = 0) {
      return listId + '_' + type + '_' + detailId
    },
    getListIdFormTabId (tabId) {
      return tabId.split('_')[0]
    },
    getDetailTypeFormTabId (tabId) {
      return tabId.split('_')[1]
    },
    getDetailIdFormTabId (tabId) {
      return Number.parseInt(tabId.split('_')[2])
    }
  }
}
</script>

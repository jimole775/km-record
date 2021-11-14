<script>
import utils from '@/utils'
import api from '@/api'
const indexKey = '_index_'
// 如果文本长度超过20，就省略掉
const cellMaxCharLen = 20
export default {
  props: {
    columns: {
      type: Array,
      default: () => []
    },
    dataApi: { // api名字，STable会以api[this.dataApi]的方式调用
      type: String | Function,
      default: null
    },
    searchor: {
      type: Array, // 查询组件定制模板
      default: () => []
    },
    dataParams: { // 插入查询参数，这个参数会触发fetch
      type: Object,
      default: null
    },
    dataDict: { // 由于数据接口的不统一，使用这个来确定列表数据在接口中的位置
      type: String,
      default: null
    },
    recordStatusField: { // 用来指定每一行数据的状态字段名, 默认'flowNode'
      type: String,
      default: 'flowNode'
    },
    expandApi: { // 如果是树级列表，点击展开的时候，需要单独的expandApi拉取子项的数据
      type: String | Function,
      default: null
    },
    deleteApi: { // 删除的接口
      type: String | Function,
      default: null
    },
    exportApi: { // 导出的接口
      type: String | Function,
      default: null
    },
    importApi: { // 导入的接口
      type: String | Function,
      default: null
    },
    templateApi: { // 下载导入模板的接口
      type: String | Function,
      default: null
    },
    abandonApi: { // 批量放弃
      type: String | Function,
      default: null
    },
    passApi: { // 批量通过
      type: String | Function,
      default: null
    },
    unpassApi: { // 批量不通过（大部分情况下，和驳回同一个接口）
      type: String | Function,
      default: null
    },
    rejectApi: { // 批量驳回
      type: String | Function,
      default: null
    },
    revokeApi: { // 批量撤回
      type: String | Function,
      default: null
    },
    transferApi: { // 批量转审
      type: String | Function,
      default: null
    },
    closeApi: { // 批量关闭
      type: String | Function,
      default: null
    },
    fetchImmediate: { // 是否立即查询数据
      type: Boolean,
      default: true
    },
    isPagination: { // 是否使用翻页
      type: Boolean,
      default: true
    },
    isSelection: { // 是否需要勾选框
      type: Boolean,
      default: true
    },
    rowKey: { // 确定每行的key绑定的字段
      type: String,
      default: 'id'
    },
    selectMode: { // 单选还是多选
      type: String,
      default: 'checkbox'
    },
    showRank: { // 显示序号
      type: Boolean,
      default: false
    },
    bridge: { // 显示序号
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      queryObj: {},
      dataList: [],
      fileList: [],
      isLoading: false,
      isSearchorExpand: true,
      searchorGroups: [], // 显示搜索栏
      selectedRows: [],
      selectedRowKeys: [],
      expandedRowKeys: [],
      columnSlots: [],
      columnScopedSlots: [],
      modal: {
        show: false,
        info: {},
        form: this.$form.createForm(this)
      },
      pagination: {
        current: 1,
        pageSize: 10,
        total: 0,
        showSizeChanger: true,
        showTotal: total => `共 ${total} 条`,
        pageSizeOptions: ['10', '20', '50', '100']
      }
    }
  },
  watch: {
    // 监听dataParams参数，使其能触发fetchData()
    dataParams: {
      handler (val) {
        if (val) {
          this.fetchData()
        }
      },
      deep: true,
      immediate: true
    },
    columns: {
      handler (val = []) {
        this.columnSlots = []
        this.columnScopedSlots = []
        this.insertIndexCol(val)
        this.flattenColumns(val, this.columnSlots, this.columnScopedSlots)
      },
      immediate: true
    }
  },
  computed: {
    modalinfomap () {
      return {
        pass: {
          type: 'pass',
          title: '通过',
          api: this.passApi,
          columns: [],
          approvalResult: '1',
          listTitle: '通过项目:',
          reasonTitle: '审批说明:',
          opreationTips: '审批成功'
        },
        reject: {
          type: 'reject',
          title: '驳回',
          api: this.rejectApi,
          columns: [],
          approvalResult: '2',
          listTitle: '驳回项目:',
          reasonTitle: '驳回原因:',
          opreationTips: '驳回成功'
        },
        unpass: {
          type: 'unpass',
          title: '不通过',
          api: this.unpassApi,
          columns: [],
          approvalResult: '3',
          listTitle: '不通过项目:',
          reasonTitle: '不通过原因:',
          opreationTips: '操作成功'
        },
        revoke: {
          type: 'revoke',
          title: '撤回',
          api: this.revokeApi,
          columns: [],
          approvalResult: '4',
          listTitle: '撤回项目:',
          reasonTitle: '撤回原因:',
          opreationTips: '撤回成功'
        },
        close: {
          type: 'close',
          title: '关闭',
          api: this.closeApi,
          columns: [],
          approvalResult: '7',
          listTitle: '关闭项目:',
          reasonTitle: '关闭原因:',
          opreationTips: '关闭成功'
        },
        abandon: {
          type: 'abandon',
          title: '放弃',
          api: this.abandonApi,
          columns: [],
          approvalResult: '10',
          listTitle: '放弃项目:',
          reasonTitle: '放弃原因:',
          opreationTips: '放弃成功'
        },
        transfer: {
          type: 'transfer',
          title: '转审',
          api: this.transferApi,
          columns: [],
          approvalResult: '8',
          listTitle: '转审项目:',
          reasonTitle: '',
          opreationTips: '转审成功'
        },
        delete: {
          type: 'delete',
          title: '删除',
          api: this.deleteApi,
          columns: [],
          approvalResult: '1',
          listTitle: '删除项目:',
          reasonTitle: '',
          opreationTips: '删除成功'
        }
      }
    },
    modalColumns () {
      const res = []
      this.columns.forEach((colItem) => {
        if (res.length < 5) {
          res.push(colItem)
        }
      })
      return res
    },
    user () {
      return this.$store.state.global.user
    },
    autoScroll () {
      const scroll = { x: 0 }
      this.countColumnsSize(this.columns, scroll)
      return scroll
    },
    currentDomain () { // '域名'
      return this.$store.getters.getCurrentDomain()
    },
    supportSeries () {
      const dicts = this.$store.getters.getDictByGroupCode('upload_file_suffix_while_list')
      const supports = dicts.map((item) => {
        return '.' + item.itemCode
      })
      return this.accept ? this.accept : supports.join(',')
    }
  },
  mounted () {
    this.fixFields()
    this.initialize()
    this.fetchImmediate && this.fetchData()
  },
  methods: {
    fixFields () {
      // 保持key和dataIndex同时存在
      this.searchor && this.searchor.forEach((item) => {
        item.key = item.key || item.dataIndex
        item.dataIndex = item.key || item.dataIndex
        item.componentName = item.component ? (item.component.name ? item.component.name : item.component) : ''
      })
      this.columns && this.columns.forEach((item) => {
        item.key = item.key || item.dataIndex
        item.dataIndex = item.key || item.dataIndex
      })
    },
    insertIndexCol (columns) {
      if (this.showRank && !hasIndexColumn(columns)) {
        columns.unshift({
          title: '序号',
          width: 60,
          dataIndex: indexKey,
          align: 'center',
          customRender: (text, record, index) => {
            return (index + 1) + (this.pagination.current - 1) * this.pagination.pageSize
          }
        })
      }
      function hasIndexColumn (columns) {
        let res = false
        for (let i = 0; i < columns.length; i++) {
          const col = columns[i]
          if (col.key === indexKey || col.dataIndex === indexKey) {
            res = true
            break
          }
        }
        return res
      }
    },
    countColumnsSize (columns, scrollObj) {
      columns && columns.forEach(col => {
        if (col.width) {
          scrollObj.x += col.width ? Number.parseFloat(col.width) : 100
        }
        if (col.children && col.children.length) {
          this.countColumnsSize(col.children, scrollObj)
        }
      })
    },
    flattenColumns (columns, columnSlots, columnScopedSlots) {
      columns && columns.forEach(col => {
        if (col.slots || col.slotsRender) {
          columnSlots.push(col)
        }
        if (col.scopedSlots || col.scopedSlotsRender) {
          columnScopedSlots.push(col)
        }
        if (!col.children && !col.customRender && !col.scopedSlots && !col.slotsRender && !col.scopedSlotsRender) {
          col.customRender = this.fixTextWrapper(this.$createElement)
        }
        if (col.children && col.children.length) {
          this.flattenColumns(col.children, columnSlots, columnScopedSlots)
        }
      })
    },
    fixTextWrapper (h) {
      return (text, record, index) => {
        if (utils.isString(text)) {
          return (<SLine len={cellMaxCharLen} value={text} />)
        } else {
          return text
        }
      }
    },
    showmodal (type) {
      // 判断有没有勾选
      if (!this.selectedRows || !this.selectedRows.length) {
        return this.$modal.warning({
          title: '提示',
          content: '请至少勾选一项！'
        })
      }
      if (hasEndStation.call(this)) {
        return this.$modal.warning({
          title: '提示',
          content: '选项中有已结束的项目，请重新选择！'
        })
      } else {
        this.modal.form.setFieldsValue({
          approvalContent: '',
          transfer: []
        })
        this.modal.info = this.modalinfomap[type]
        this.modal.show = true
      }
      function hasEndStation () {
        let yes = false
        this.selectedRows.forEach((row) => {
          if (row[this.recordStatusField] === 'end') {
            yes = true
          }
        })
        return yes
      }
    },
    modalSubmitEvent () {
      this.modal.form.validateFields(async (err, values) => {
        if (err) return
        const modalInfo = this.modal.info || {}
        const params = {
          approvalResult: modalInfo.approvalResult,
          instanceIds: this.selectedRowKeys,
          ids: this.selectedRows.map(item => item.id),
          currentAccount: this.user.employeeNumber,
          currentName: this.user.name
        }
        // 专门处理转审的参数
        if (values.transfer) {
          params['transferAccount'] = utils.splitUser(values.transfer)[0]
          params['transferName'] = utils.splitUser(values.transfer)[1]
          params['ids'] = this.selectedRows.map(row => row.id)
        }
        if (!modalInfo.api) {
          throw new Error('STable未绑定对应的接口！', modalInfo)
        }
        const res = await this.getApiFunction(modalInfo.api)({
          ...values,
          ...params
        })
        if (res.code === 200) {
          this.$message.success(modalInfo.opreationTips)
          this.reload()
          this.$emit('update')
        } else {
          this.$modal.warning({
            title: '提示',
            content: res.message
          })
        }
        this.modal.show = false
      })
    },
    initialize () {
      this.searchorGroups = []
      this.searchor.forEach((searchItem) => {
        this.searchorGroups.push(searchItem)
        if (searchItem.beforeRender) {
          searchItem.beforeRender(this.queryObj, searchItem, this)
        }
        if (searchItem.key) {
          this.$set(this.queryObj, searchItem.key, searchItem.default)
          if (searchItem.default) {
            this.simpleSelectEvent(searchItem.default, null, searchItem)
          }
        }
        if (searchItem.keys) {
          this.multiSelectEvent(searchItem.default, null, searchItem)
        }
      })
    },
    simpleSelectEvent (e, optionItem, searchItem) {
      // 赋值元素视图
      const value = e && e.currentTarget ? e.currentTarget.value : e
      this.setComponentView(searchItem, value)
      this.cacheDefaultView(searchItem, value)
      // 重置操作
      if (utils.isNone(value) || utils.isEmptyArray(value) || utils.isEmptyObject(value)) {
        this.queryObj[searchItem.key] = null
        return this.queryObj
      }

      if (isLabelOption(value)) {
        const userOption = value.length ? JSON.parse(value[0].key) : null
        this.queryObj[searchItem.key] = userOption ? userOption['key'] : null
      } else {
        this.queryObj[searchItem.key] = value
      }
      function isLabelOption (value) {
        return (utils.isArray(value) && value.length && value[0].label && value[0].key)
      }
    },
    // 有两类选项
    multiSelectEvent (value, optionItem, searchItem) {
      // 赋值元素视图
      this.setComponentView(searchItem, value)
      // 暂存value
      this.cacheDefaultView(searchItem, value)

      // 重置操作
      if (utils.isNone(value) || utils.isEmptyArray(value) || utils.isEmptyObject(value)) {
        return searchItem.keys.forEach((key, index) => {
          this.queryObj[key] = null
        })
      }

      // 主要场景 UserSelect
      if (searchItem.componentName === 'UserSelect') {
        // userSelect的选项被构造了一次，需要重新解构出来
        const userOption = value.length ? JSON.parse(value[0].key) : null
        searchItem.keys.forEach((key, index) => {
          const optionKey = searchItem.optionKeys[index]
          this.queryObj[key] = userOption ? userOption[optionKey] : null
        })
      }

      // 主要场景：DepatmentSelect
      if (searchItem.componentName === 'DepatmentSelect') {
        searchItem.keys.forEach((key, index) => {
          const optionKey = searchItem.optionKeys[index]
          this.queryObj[key] = optionItem ? optionItem[optionKey] : null
        })
      }

      // value = 'Array', optionItem = 'Array' => Select multi, RangPicker
      if (utils.isArray(value) && utils.isArray(optionItem)) {
        searchItem.keys.forEach((key, index) => {
          this.queryObj[key] = optionItem[index] || null
        })
      }
    },
    async expandEvent (opr, record) {
      if (opr && this.expandApi) {
        this.expandedRowKeys.push(record[this.rowKey])
        const res = await this.getApiFunction(this.expandApi)(this.formatQueryObj({ ...record }))
        if (res.code === 200) {
          if (res.data) {
            const children = this.evalHandle(res.data)

            // 关联父级节点数据
            const cpyParent = { ...record }
            delete cpyParent.children
            children.forEach((child) => {
              child.parentId = cpyParent[this.rowKey]
              child.parent = cpyParent
            })

            // 把子节点插入整棵树
            this.insertTreeNode(this.dataList, record[this.rowKey], children)

            // 刷新数据
            this.update()
          }
        } else {
          this.$modal.warning({
            title: '提示',
            okText: '确定',
            content: res.message
          })
        }
      }
      if (!opr) {
        // 收起时，把 record 从 this.expandedRowKeys 中剔除
        this.spliceExpandRowKeys(record)
      }
    },
    spliceExpandRowKeys (record) {
      for (let index = 0; index < this.expandedRowKeys.length; index++) {
        const key = this.expandedRowKeys[index]
        if (key === record[this.rowKey]) {
          this.expandedRowKeys.splice(index, 1)
          break
        }
      }
    },
    update () {
      this.$emit('update', this.dataList)
    },
    insertTreeNode (loopNodes, insertNodeId, willInsertNodes, resolve) {
      for (let index = 0; index < loopNodes.length; index++) {
        const loopNode = loopNodes[index]
        if (loopNode[this.rowKey] === insertNodeId) {
          // 先把子项从 this.expandedRowKeys 中剔除，再插入树中
          willInsertNodes.forEach((node) => {
            this.spliceExpandRowKeys(node)
          })
          loopNode.children = willInsertNodes
          return false
        }
        if (utils.isArray(loopNode.children) && loopNode.children.length) {
          this.insertTreeNode(loopNode.children, insertNodeId, willInsertNodes, resolve)
        }
      }
    },
    // table全选功能
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
      this.$emit('selectChange', selectedRowKeys, selectedRows)
    },
    // 重置
    async resetSearch () {
      // 充填必填的搜索项，选取默认值
      this.searchor.forEach((searchItem) => {
        if (!searchItem.required) {
          if (searchItem.key) {
            this.resetByFieldType(this.queryObj, searchItem.key)
          }
          if (searchItem.keys) {
            searchItem.keys.forEach((key) => {
              this.resetByFieldType(this.queryObj, key)
            })
          }
          // 置空 default，避免重新渲染的时候会进行默认赋值
          this.resetByFieldType(searchItem, 'default')
        }
      })
      this.pagination.current = 1
      this.fetchData()
    },
    // 设置组件的视图
    // ****************************************
    // * 注意：这个函数会触发组件的change事件
    // * 所以，谨慎在change事件函数中对
    // * “searchItem.value” 或者 “searchItem.default”
    // * 字段进行赋值操作，会造成死循环
    // ****************************************
    setComponentView (searchItem, view) {
      const ref = this.spillComponentRef(searchItem)
      const comp = this.$refs[ref]
      if (comp) {
        if (utils.isObject(comp)) {
          comp.value = view // 会触发change事件
        }
        if (utils.isArray(comp)) {
          comp[0].value = view // 会触发change事件
        }
      } else {
        return setTimeout(() => {
          this.setComponentView(searchItem, view)
        }, 150)
      }
    },
    // 暂存组件的视图,帮助“required”字段在刷新时不会被刷掉
    cacheDefaultView (searchItem, view) {
      searchItem.default = view
    },
    // 根据value类型，进行置空操作
    resetByFieldType (obj, key) {
      if (utils.isString(obj[key])) {
        obj[key] = ''
      }
      if (utils.isNumber(obj[key])) {
        obj[key] = null
      }
      if (utils.isObject(obj[key])) {
        obj[key] = {}
      }
      if (utils.isArray(obj[key])) {
        obj[key] = []
      }
    },
    // 导入
    async beforeUpload (file) {
      const pass = utils.verifyUploadType(file.name, this.supportSeries)
      if (!pass) return false
      if (!this.importApi) return false
      const params = new FormData()
      params.append('file', file)
      const res = await this.getApiFunction(this.importApi)(params)
      if (res.code === 200) {
        this.$message.success('导入成功')
        this.fetchData()
      } else {
        this.$modal.warning({
          title: '提示',
          okText: '确定',
          content: res.message
        })
      }
      return false
    },
    /**
     * @injectParam 一般是由父级组件调用时，传入的
     */
    search (injectParam = {}) {
      this.pagination.current = 1
      this.fetchData({ ...injectParam })
    },
    /**
     * 提供语义化接口，功能和fetchData一致
     */
    reload () {
      this.fetchData()
    },
    formatQueryObj (injectparams) {
      const queryParams = JSON.parse(JSON.stringify({ ...this.queryObj }))
      // 处理 UserSelect 组件的取值
      // UserSelect 有两种用法
      // 1. searchItem.key 只获取一个值，选中项是个数据，需要format处理，默认只获取code
      // 2. searchItem.keys 获取多个值，但是 this.multiSelectEvent 已经对取值进行处理了
      // 原始取值样例：[{key: "{"key":"51000001","label":"Hongkui Yang"}", label: "51000001 Hongkui Yang"}]
      this.searchor.forEach((searchItem) => {
        if (searchItem.componentName === 'UserSelect') {
          if (searchItem.key && utils.isArray(queryParams[searchItem.key])) {
            if (utils.isArray(queryParams[searchItem.key])) {
              if (queryParams[searchItem.key][0]) {
                const itemOption = JSON.parse(queryParams[searchItem.key][0].key)
                queryParams[searchItem.key] = itemOption.key
              }
            }
          }
        }
      })

      // 转换 Moment 类型的值
      Object.keys(queryParams).forEach((key) => {
        if (queryParams[key] instanceof utils.moment) {
          queryParams[key] = utils.date2YMD(queryParams[key])
        }
      })

      // 手动清理空值的字段
      Object.keys(queryParams).forEach((key) => {
        if (queryParams[key] === '' || queryParams[key] === null || queryParams[key] === undefined) {
          delete queryParams[key]
        }
        if (utils.isEmptyArray(queryParams[key]) || utils.isEmptyObject(queryParams[key])) {
          delete queryParams[key]
        }
      })

      // 分页参数
      const pageParam = {
        pageSize: this.pagination.pageSize,
        pageNum: this.pagination.current
      }
      // 【queryParams】来源：
      //    页面上的搜索栏
      // 【injectparams】来源：
      //    当外部直接调用this.search方法时，有可能注入额外参数
      //    或者当前是树级表格，点击展开触发的this.expandEvent方法，会把当前行数据当作参数传入
      // 【this.dataParams】来源：
      //    由父级组件定制，当前组件不会对这个数据进行过滤，所以定制时，保持数据的纯净（可以直接交到后端）
      return this.handleParamsByCustom({ ...queryParams, ...injectparams, ...this.dataParams, ...pageParam })
    },

    // 最后交给定制的回调参数进行调整
    handleParamsByCustom (finalParams) {
      this.searchor.forEach((searchItem) => {
        if (searchItem.beforeSubmit) {
          searchItem.beforeSubmit(finalParams, this)
        }
      })
      return finalParams
    },

    // 导出
    exportOut () {
      if (this.dataList.length === 0) {
        return this.$modal.warning({
          title: '提示',
          okText: '确定',
          content: '暂无数据导出!'
        })
      }
      // eslint-disable-next-line no-unused-vars
      const ids = []
      if (this.selectedRows && this.selectedRows.length > 0) {
        this.selectedRows.filter(item => {
          ids.push(item.id)
        })
        // ids = ids.substring(0, ids.length - 1)
      }
      this.getApiFunction(this.exportApi)(this.formatQueryObj({ selectedRows: this.selectedRows, ids }))
    },
    // 导入模板下载
    downLoadTemplate () {
      if (api[this.templateApi] && utils.isFunction(api[this.templateApi])) {
        api[this.templateApi]()
      } else {
        utils.exportGetFile(this.templateApi)
      }
    },
    getApiFunction (apiNameOrFunction) {
      if (utils.isFunction(apiNameOrFunction)) {
        return apiNameOrFunction
      }
      if (utils.isString(apiNameOrFunction)) {
        return api[apiNameOrFunction] || function () {}
      }
      if (utils.isUndefined(apiNameOrFunction)) {
        return function () {}
      }
    },
    evalHandle (data) {
      let res = {}
      if (this.$props.dataDict &&
        utils.isString(this.$props.dataDict)) {
        res = eval('data' + '.' + this.$props.dataDict)
      } else {
        res = data
      }
      return res
    },
    detectTotal (data) {
      let pageObj = data
      if (this.$props.dataDict &&
        utils.isString(this.$props.dataDict)) {
        // 一般后端的模型，都把分页数据放在了实例数据的同一层结构
        // 比如：res.data.pageinfo.records
        // 那么：res.data.pageinfo.total
        const dicts = this.$props.dataDict.split('.')
        if (dicts && dicts.length > 1) {
          dicts.pop()
          pageObj = eval('data' + '.' + dicts.join())
        }
      }
      return pageObj.total || 0
    },
    // 获取列表数据
    async fetchData (injectparams = {}) {
      if (this.isLoading) return false
      if (!this.dataApi) return false
      this.isLoading = true
      this.selectedRows = []
      this.selectedRowKeys = []
      const res = await this.getApiFunction(this.dataApi)(this.formatQueryObj(injectparams))
      this.isLoading = false
      if (res.code === 200) {
        if (res.data) {
          this.dataList = this.evalHandle(res.data)
          this.pagination.total = this.detectTotal(res.data)
          this.expandedRowKeys = []
        } else {
          this.dataList = []
          this.pagination.total = 0
        }
        this.update()
      } else {
        this.$modal.warning({
          title: '提示',
          okText: '确定',
          content: res.message
        })
      }
    },
    // 服务费用分页
    onChangePage (val) {
      this.pagination.current = val.current
      this.pagination.pageSize = val.pageSize
      this.fetchData()
    },
    spillComponentRef (searchItem) {
      return `${searchItem.componentName}${searchItem.key ? searchItem.key : searchItem.keys[0]}`
    }
  },
  render (h) {
    const batchHandleButtons = buildBatchHandleButtons.call(this, h)
    const summaryButtons = buildsummaryBaseButtons.call(this, h)
    const batchHandleModal = buildModal.call(this, h)
    const mainTable = buildMainTable.call(this, h)
    const searchorGroup = buildSearchorGroup.call(this, h)
    const summarySlots = getSummarySlots.call(this, h)
    return (
      <div>
        { searchorGroup }
        <div class={'panel-content'}>
          {
            hasSummary(summarySlots, batchHandleButtons, summaryButtons) &&
            <div class={'btn-wrap clearfix'}>
              { ...summarySlots }
              { ...batchHandleButtons }
              { ...summaryButtons }
            </div>
          }
        </div>
        <div>{ mainTable }</div>
        <div>{ batchHandleModal }</div>
      </div>
    )
    function hasSummary (summarySlots, batchHandleButtons, summaryButtons) {
      return !!(summarySlots.length || batchHandleButtons.length || summaryButtons.length)
    }
  }
}

// 获取插槽提供的按钮
function getSummarySlots () {
  const slots = this.$slots || {}
  return slots.summary || []
}

// 创建批处理按钮
function buildBatchHandleButtons (h) {
  return Object.keys(this.modalinfomap).map((key) => {
    const buttonItem = this.modalinfomap[key]
    if (buttonItem.api) {
      return (
        <a-button ghost type={'primary'} onClick={() => this.showmodal(buttonItem.type)}>
          <span>{ buttonItem.title }</span>
        </a-button>
      )
    } else {
      return null
    }
  }).filter(item => item)
}

// 创建基础按钮 （导入，导出，下载模板）
function buildsummaryBaseButtons (h) {
  const buttons = []
  if (this.importApi) {
    buttons.push(
      <a-upload
        name={'file'}
        accept={'.xls, .xlsx'}
        before-upload={this.beforeUpload}
        file-list={this.fileList}
        class={'import-table'}
      >
        <a-tooltip>
          <template slot={'title'}>导入</template>
          <a-button
            class={'cir-button button-import'}
          />
        </a-tooltip>
      </a-upload>
    )
  }
  if (this.exportApi) {
    buttons.push(
      <a-tooltip>
        <template slot={'title'}>导出</template>
        <a-button
          onClick={() => this.exportOut()}
          class={'cir-button button-export'}
        />
      </a-tooltip>
    )
  }
  if (this.templateApi) {
    buttons.push(
      <a-tooltip>
        <template slot={'title'}>导入模板下载</template>
        <a-button
          onClick={() => this.downLoadTemplate()}
          class={'cir-button button-import-template-down'}
        />
      </a-tooltip>
    )
  }
  return buttons
}

// 创建弹出框
function buildModal (h) {
  return (
    <a-modal
      width={'60%'}
      title={'批量操作'}
      v-model={this.modal.show}
      onOk={this.modalSubmitEvent}
    >
      <a-form form={this.modal.form}>
        <a-row>
          {
            this.modal.info.type === 'transfer' &&
            <a-col>
              <a-form-item label="转审人" label-col={{ span: 3 }} wrapper-col={{ span: 18 }}>
                <UserSelect v-decorator={['transfer', { rules: [{ required: true, message: '请选择转审人' }] }]} />
              </a-form-item>
            </a-col>
          }
          {
            this.modal.info.reasonTitle &&
            <a-col>
              <a-form-item label={this.modal.info.reasonTitle} label-col={{ span: 3 }} wrapper-col={{ span: 18 }}>
                <a-textarea rows={4} v-decorator={['approvalContent', { rules: [{ required: true, message: `请填写${this.modal.info.reasonTitle}` }] }]} />
              </a-form-item>
            </a-col>
          }
        </a-row>
        <a-row>
          <a-col>
            <a-form-item label={this.modal.info.listTitle || ''} label-col={{ span: 3 }} wrapper-col={{ span: 18 }}>
              <a-table
                bordered
                row-key={'id'}
                columns={this.modalColumns}
                data-source={this.selectedRows}
                pagination={false}
              />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-modal>
  )
}

// 创建主表格
function buildMainTable (h) {
  const slots = []
  const scopedSlots = {}
  /* 表头渲染 */
  this.columnSlots.map((columnSlot, index) => {
    const slotName = (columnSlot.slots && columnSlot.slots.title) || ''
    if (columnSlot.slotsRender) {
      slots.push(<span slot={slotName}>{columnSlot.slotsRender(h, this)}</span>)
    } else {
      slots.push(<span slot={slotName}>...</span>)
    }
  })
  /* 表身渲染 */
  this.columnScopedSlots.map(columnSlot => {
    const slotName = (columnSlot.scopedSlots && columnSlot.scopedSlots.customRender) || columnSlot.dataIndex || columnSlot.key
    scopedSlots[slotName] = function (text, record, index) {
      if (columnSlot.scopedSlotsRender) {
        return columnSlot.scopedSlotsRender(h, record, this)
      } else {
        return text
      }
    }
  })
  return (
    <a-table
      bordered
      scopedSlots={scopedSlots}
      columns={this.columns}
      data-source={this.dataList}
      pagination={this.isPagination ? this.pagination : false}
      scroll={this.autoScroll}
      row-key={this.rowKey}
      row-selection={this.isSelection ? { 'type': this.selectMode, 'selectedRowKeys': this.selectedRowKeys, 'onChange': this.onSelectChange } : null}
      expanded-row-keys={this.expandedRowKeys}
      onExpand={this.expandEvent}
      onChange={this.onChangePage}
    >
      { ...slots }
    </a-table>
  )
}

function buildSearchorGroup (h) {
  if (!this.searchorGroups || !this.searchorGroups.length) return ''
  return (
    <div class={['panel-content', 'border-bottom-1']}>
      <a-form class={['form-wrap']}>
        <a-row>
          {
            buildSearchItems.call(this)
          }
          {
            buildSearchButton.call(this)
          }
        </a-row>
      </a-form>
    </div>
  )

  function buildSearchItems () {
    if (this.searchorGroups && this.searchorGroups.length) {
      return this.searchorGroups
        .filter((item, index) => filterItems.call(this, index))
        .map(searchItem => {
          return (
            <a-col span={ searchItem.layout ? searchItem.layout.span : 6 } >
              <a-form-item
                label={searchItem.title}
                label-col={{ span: searchItem.layout ? searchItem.layout.label : 8 }}
                wrapper-col={{ span: searchItem.layout ? searchItem.layout.wrapper : 16 }}
              >
                {
                  createFormItem.call(this, searchItem)
                }
              </a-form-item>
            </a-col>
          )
        })
    } else {
      return ''
    }
  }

  function createFormItem (searchItem) {
    return <searchItem.component
      props={searchItem.props}
      attrs={searchItem.attrs}
      dom-attrs={searchItem.domAttrs}
      allow-clear={!searchItem.required}
      value={searchItem.default}
      ref={this.spillComponentRef(searchItem)}
      depend={this.queryObj[searchItem.dependKey]}
      onKeyup={(e) => /13/.test(e.keyCode) && this.fetchData()}
      onChange={
        (value, optionItem) => {
          searchItem.key
            ? this.simpleSelectEvent(value, optionItem, searchItem)
            : this.multiSelectEvent(value, optionItem, searchItem)
        }
      }
    />
  }

  function buildSearchButton () {
    return (
      <a-col span={this.searchorGroups.length < 4 ? 8 : 24} class={['t-center', 'mt5']}>
        <a-button ghost type={'primary'} onClick={() => this.search()}>查询</a-button>
        <a-button style={{ margin: '0 8px' }} onClick={() => this.resetSearch()}>重置</a-button>
        {
          this.searchorGroups.length > 4 &&
          <a
            style={{ 'color': '#999', 'font-size': '0.8rem' }}
            onClick={() => { this.isSearchorExpand = !this.isSearchorExpand }}
          >
            { this.isSearchorExpand ? '收起' : '展开' }
            <a-icon class={this.isSearchorExpand ? 'trans-reverse' : 'trans'} type={'double-right'} />
          </a>
        }
      </a-col>
    )
  }
  // 返回true展示，返回false隐藏
  function filterItems (index) {
    // 如果下标小于4，返回true
    if (index < 4) {
      return true
    }
    // 如果下标大于4，且是展开状态，返回false
    if (index >= 4 && this.isSearchorExpand) {
      return true
    }
  }
}

</script>
<style lang="less" scoped>
.trans {
  transform: rotate(90deg);
}
.trans-reverse {
  transform: rotate(270deg);
}
div.ant-table-wrapper {
  padding: 0;
  background-color: #fff;
}
</style>

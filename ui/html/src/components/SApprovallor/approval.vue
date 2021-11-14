<template>
  <div>
    <ApprovalStepBar
      :id="recordData.flowInstanceId"
      @update="updateCurrentNode"
    />
    <a-collapse
      :bordered="false"
      :active-key="['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']"
    >
      <template v-for="(componentItem, index) in activeComponents">
        <a-collapse-panel
          v-if="componentItem.show"
          :header="componentItem.title"
          :key="`${index + 1}`"
          class="m-block"
        >
          <component
            :ref="`${componentItem.componentName}_${index}`"
            :is="componentItem.component"
            :mode="componentItem.mode"
            :active-components="activeComponents"
            :form-items="componentItem.formItems"
            :component-item="componentItem"
            :operation-item="componentItem.operationItem"
            :data-source="basicData"
            :tab-proxy="tabProxy"
            :current-node="currentNode"
            :columns="componentItem.columns"
            :before-render="beforeRender"
            :business-id="recordData.id"
            :business-type="apimap.logType"
            :bridge="{
              ...bridge,
              apimap,
              tabProxy,
              recordData,
              currentNode,
              componentItem,
              activeComponents,
              datasource: basicData,
              columns: componentItem.columns,
              formItems: componentItem.formItems,
              operationItem: componentItem.operationItem,
            }"
            @submit="submitHandler"
          />
        </a-collapse-panel>
      </template>
    </a-collapse>
  </div>
</template>
<script>
import api from '@/api'
import utils from '@/utils'
import baseMixins from '@/mixins/baseMixins.js'
import ApprovalStepBar from '@/components/ApprovalStepBar'
export default {
  components: {
    ApprovalStepBar
  },
  mixins: [baseMixins],
  props: {
    tabProxy: {
      type: Object,
      required: true
    },
    approvalConfig: {
      type: Object,
      required: true
    },
    apimap: {
      type: Object,
      required: true
    },
    bridge: {
      type: Object,
      default: () => ({})
    },
    beforeRender: {
      type: Function,
      default: p => p
    },
    beforeSubmit: {
      type: Function,
      default: p => p
    }
  },
  data () {
    return {
      currentPane: {},
      basicData: {},
      currentNode: {},
      activeComponents: [],
      form: this.$form.createForm(this)
    }
  },
  watch: {
    activeModule: {
      async handler (aModule) {
        if (!aModule) return []
        const components = this.isApprovallor
          ? aModule.components.permission
          : aModule.components.dispermission
        this.activeComponents = components.map((item) => {
          if (utils.isString(item.component)) {
            item.componentName = item.component
          }
          if (utils.isObject(item.component)) {
            item.componentName = item.component.name || 'customRender'
          }
          if (utils.isNone(item.component)) {
            item.componentName = 'customRender'
          }
          return item
        })
      },
      immediate: true,
      deep: true
    },
    tabProxy: {
      async handler (tabProxy) {
        if (!tabProxy) return false
        const activePane = tabProxy.panes.filter((pane) => pane.tabId === tabProxy.activeId)
        this.currentPane = activePane ? activePane[0] : {}
        const res = await api[this.apimap.detail](this.currentPane.recordData)
        if (res.code === 200) {
          this.basicData = { ...res.data }
        } else {
          this.$message.warning(res.message)
        }
      },
      immediate: true
    }
  },
  computed: {
    recordData () {
      return this.currentPane.recordData || {}
    },
    isApprovallor () {
      return this.currentNode &&
        this.currentNode.approvalAccountList &&
          this.currentNode.approvalAccountList.includes(this.currentAccount)
    },
    activeModule () {
      return this.approvalConfig && this.approvalConfig[this.currentNode.nodeCode]
    }
  },
  methods: {
    updateCurrentNode (node) {
      this.currentNode = node
    },
    // 获取每个模块的form数据
    async getComponentsValues () {
      const params = {}
      const tips = []
      for (let index = 0; index < this.activeComponents.length; index++) {
        const componentItem = this.activeComponents[index]
        if (componentItem.show === false) continue
        const componentDomId = `${componentItem.componentName}_${index}`
        if (componentItem.mode === 'edit') {
          await this.$refs[componentDomId]
          const validRes = await this.$refs[componentDomId][0].getFieldsValue()
          if (validRes.type === 'success') {
            Object.assign(params, validRes.data)
          } else {
            tips.push(validRes.message)
          }
        }
      }
      return Promise.resolve({ params, tips })
    },
    getComponentsRequiredFields (params) {
      let requiredFields = []
      this.activeComponents.forEach((component) => {
        if (component.component === 'ApprovalOperation' ||
          component.componentName === 'ApprovalOperation') {
          const inputs = component.operationItem.inputs || []
          inputs.forEach((item) => {
            if (item.permissions.includes(params.approvalResult)) {
              if (item.required === true) {
                if (item.paramKeys) {
                  requiredFields = [...requiredFields, ...item.paramKeys]
                } else if (item.key) {
                  // 如果没有 item.paramKeys，默认就是 item.key
                  requiredFields.push(item.key)
                }
              }
            }
          })
        }
      })
      return requiredFields
    },
    validateRequiredField ({ tips, params }) {
      const requiredFields = this.getComponentsRequiredFields(params)
      let isFinishRequiredField = true
      // 操作模块的必填字段验证
      if (requiredFields.length) {
        requiredFields.forEach((field) => {
          if (utils.isNone(params[field])) {
            isFinishRequiredField = false
          }
        })
      }
      // 如果选择 “通过”，tips有值的话，就代表必填条件未完成
      if (params.approvalResult === '1' && tips.length) {
        isFinishRequiredField = false
      }
      return isFinishRequiredField
    },
    async submitHandler () {
      const values = await this.getComponentsValues()
      if (this.validateRequiredField(values)) {
        this.startApprove({
          ...values.params,
          id: this.recordData.id,
          instanceId: this.basicData.flowInstanceId,
          currentFlowNode: this.basicData.flowNode
        })
      } else {
        this.$modal.warning({
          title: '提示',
          content: values.tips[0] || '请完成必填字段!'
        })
      }
    },
    // 发起审批
    async startApprove (params) {
      const cparams = this.$props.beforeSubmit(params, this)
      const res = await api[this.apimap.approval](cparams)
      if (res.code === 200) {
        this.$message.success('操作成功')
        this.$emit('close')
      } else {
        this.$modal.warning({
          title: '提示',
          content: res.message
        })
      }
    }
  }
}
</script>
<style lang="less" scoped>
.ppproject-footer {
  text-align: center;
  margin: 2rem 0;
  button {
    width: 16rem;height:2.6rem;
  }
}
/deep/.ant-row {
  line-height: 2.5;
}
</style>

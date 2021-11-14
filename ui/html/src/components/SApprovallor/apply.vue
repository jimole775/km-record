<template>
  <div>
    <a-collapse
      :bordered="false"
      :active-key="['1','2','3','4','5']"
    >
      <template v-for="(componentItem, index) in activeComponents">
        <a-collapse-panel
          :header="componentItem.title"
          :key="`${index + 1}`"
          class="m-block"
        >
          <component
            :ref="`${componentItem.componentName}_${index}`"
            :is="componentItem.component"
            :operation-item="componentItem.operationItem"
            :before-render="beforeRender"
            :before-submit="beforeSubmit"
            :form-items="componentItem.formItems"
            :active-components="activeComponents"
            :mode="componentItem.mode"
            :tab-proxy="tabProxy"
            :bridge="{
              ...bridge,
              apimap,
              tabProxy,
              applyConfig,
              componentItem,
              activeComponents,
              columns: componentItem.columns,
              formItems: componentItem.formItems,
              operationItem: componentItem.operationItem,
            }"
          />
        </a-collapse-panel>
      </template>
    </a-collapse>
    <div class="ppproject-footer">
      <a-button type="primary" ghost @click="emitApply">发起</a-button>
    </div>
  </div>
</template>
<script>
import api from '@/api'
import utils from '@/utils'
export default {
  props: {
    applyConfig: {
      type: Object,
      required: true
    },
    apimap: {
      type: Object,
      required: true
    },
    tabProxy: {
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
      activeComponents: []
    }
  },
  watch: {
    applyConfig: {
      handler (aModulesMap) {
        const components = aModulesMap.components || []
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
    }
  },
  methods: {
    async emitApply () {
      const { successData, failureTips } = await this.getComponentsFieldsValue()
      if (failureTips.length) {
        return this.$modal.warning({
          title: '提示',
          content: failureTips[0]
        })
      }
      const params = {
        ...successData
      }
      this.startApprove(params)
    },
    // 发起审批
    async startApprove (params) {
      const cparams = this.$props.beforeSubmit(params, this)
      const res = await api[this.apimap.apply](cparams)
      if (res.code === 200) {
        this.$message.success('操作成功')
        this.$emit('close')
      } else {
        this.$modal.warning({
          title: '提示',
          content: res.message
        })
      }
    },
    getComponentsFieldsValue () {
      return new Promise(async (resolve) => {
        let successData = {}
        const failureTips = []
        for (let index = 0; index < this.activeComponents.length; index++) {
          const component = this.activeComponents[index]
          const componentDom = await this.$refs[`${component.componentName}_${index}`][0]
          const editData = await componentDom.getFieldsValue()
          if (editData.type === 'failure') {
            failureTips.push(editData.message)
          } else {
            successData = { ...successData, ...editData.data }
          }
        }
        return resolve({ failureTips, successData })
      })
    },
    scrollTo (id) {
      const targetDom = document.querySelector('#' + id)
      if (!targetDom) return false
      targetDom.style.borderColor = '#ff0000'
      targetDom.style.transition = 'border 3s'
      setTimeout(() => {
        targetDom.style.borderColor = '#d9d9d9'
      }, 3000)
      const link = document.createElement('a')
      link.style.display = 'none'
      link.href = '#' + id
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    updateDataSet (val) {
      console.log(val)
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

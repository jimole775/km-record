<script>
import utils from '@/utils'
import { mapState } from 'vuex'
export default {
  name: 'FormItemRender',
  props: {
    dataSource: {
      type: Object,
      default: () => ({})
    },
    formItems: {
      type: Array,
      default: () => ([])
    },
    beforeRender: {
      type: Function,
      default: p => p
    },
    afterRender: {
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
      form: this.$form.createForm(this)
    }
  },
  watch: {
    formItems: {
      handler (formItems) {
        if (formItems && formItems.length) {
          this.initialize()
        }
      },
      immediate: true
    },
    dataSource: {
      handler (data) {
        if (data && Object.keys(data).length) {
          this.initialize()
        }
      },
      immediate: true
    }
  },
  computed: {
    ...mapState({
      user: state => state.global.user,
      roleType: state => state.global.userRole.type
    }),
    edit () {
      return this.mode === 'edit'
    },
    isOutsideStuff () {
      return this.roleType === 'SUPPLIER' || this.roleType === 'OUT'
    },
    readonly () {
      return this.mode === 'readonly'
    }
  },
  created () {
    this.initialize()
  },
  methods: {
    initialize () {
      const dataSource = this.dataSource
      const formItems = this.formItems

      this.formatFormItems(formItems)

      // 全局统一的默认值
      this.bindDefaultValue(dataSource, formItems)

      // 为特殊组件赋值
      utils.bindDefaultValueForComponent(dataSource, formItems)

      this.$nextTick(() => {
        this.$props.beforeRender(dataSource, formItems, this)
      })

      // this.triggeringChangeCallback(dataSource, formItems)
    },
    labelRender (h, formItem) {
      let labelC = null
      if (formItem.label) {
        labelC = h('span', { slot: 'label' }, formItem.label)
      }
      if (formItem.labelCustomRender) {
        labelC = formItem.labelCustomRender(h, formItem, this)
      }
      return labelC
    },
    wrapperRender (h, formItem) {
      if (formItem.wrapperCustomRender) {
        return formItem.wrapperCustomRender(this.$createElement, formItem, this)
      } else if (formItem.component) {
        return (<formItem.component
          props={formItem.props}
          attrs={formItem.attrs}
          domProps={formItem.domProps}
          disabled={formItem.mode === 'readonly'}
          vDecorator={[formItem.key, { initialValue: formItem.value, rules: [{ required: formItem.required, message: `请确认必填项` }] }]}
          onChange={(val) => this.componentChangeEvent(val, formItem)}
        >
          {
            // formItem.customRender && formItem.customRender(this.$createElement)
          }
        </formItem.component>)
      } else {
        return (<span
          props={formItem.props}
          attrs={formItem.attrs}
          domProps={formItem.domProps}
        > { formItem.value } </span>)
      }
    },
    bindDefaultValue (dataSource, items) {
      items.forEach((item) => {
        item.value = utils.isValuable(dataSource[item.key]) ? dataSource[item.key] : item.value
      })
    },
    componentChangeEvent (val, item) {
      item.change && item.change(val, item, this)
      this.$emit('change', val, item, this)
    },
    triggeringChangeCallback (dataSource, items) {
      items.forEach((item) => {
        item.change && item.change(item.value, item, this)
      })
    },
    validateRequiredField () {
      const tips = []
      // 操作模块的必填字段验证
      const fieldsValue = this.form.getFieldsValue()
      for (let i = 0; i < this.formItems.length; i++) {
        const formItem = this.formItems[i]
        // 只有在 required 和 show 同时为 true 时，才进行必填校验
        if (formItem.required && formItem.show) {
          if (formItem.keys) {
            if (
              isNoneFromKeys(formItem.keys) &&
              isNoneFromValue(formItem.value) &&
              isNoneFromParams(formItem.params)
            ) {
              tips.push(`请确认"${formItem.label}"！`)
              break
            }
          } else {
            if (
              isNoneForKey(formItem.key) &&
              isNoneFromValue(formItem.value) &&
              isNoneFromParams(formItem.params)
            ) {
              tips.push(`请确认"${formItem.label}"！`)
              break
            }
          }
        }
      }

      return tips

      function isNoneFromValue (value) {
        return utils.isNone(value)
      }

      function isNoneForKey (key) {
        return utils.isNone(fieldsValue[key])
      }

      function isNoneFromKeys (keys) {
        let res = false
        keys.forEach((key) => {
          if (utils.isNone(fieldsValue[key])) {
            res = true
          }
        })
        return res
      }

      function isNoneFromParams (params) {
        return utils.isEmpty(params)
      }
    },
    // 填充每个formItem的默认字段
    formatFormItems (formItems) {
      const layout8 = {
        span: 8,
        label: 9,
        wrapper: 12
      }
      formItems.forEach((item) => {
        if (item.show === undefined) this.$set(item, 'show', true)
        if (item.required === undefined) this.$set(item, 'required', false)
        if (item.layout === undefined) this.$set(item, 'layout', layout8)
        if (item.mode === undefined) this.$set(item, 'mode', 'edit')
        if (item.value === undefined) this.$set(item, 'value', null)
        if (item.params === undefined) this.$set(item, 'params', {})
        if (item.userPermissions === undefined) this.$set(item, 'userPermissions', [1, 2]) // 1是内部员工，2是外部员工
        if (item.radioPermissions === undefined) this.$set(item, 'radioPermissions', [1]) // 1通过
      })
    },
    isCanShow (formItem) {
      let res = true
      if (formItem.show === false) {
        res = false
      }
      if (this.isOutsideStuff && !(formItem.userPermissions.includes(2))) {
        res = false
      }
      return res
    },
    getFormItemsValue (formItems) {
      const res = {}
      formItems.forEach((item) => {
        if (item.keys) {
          item.keys.forEach((key) => {
            res[key] = item.value
          })
        } else {
          res[item.key] = item.value
        }
      })
      return res
    },
    mergeFormItemsParams (formItems) {
      let res = {}
      formItems.forEach((item) => {
        res = utils.merge(res, item.params)
      })
      return res
    },
    getFieldsValue () {
      return new Promise((resolve) => {
        const tips = this.validateRequiredField()
        if (tips && tips.length) {
          return resolve({
            type: 'failure',
            data: null,
            message: tips[0]
          })
        }
        this.form.validateFields((err, values) => {
          if (err) {
            resolve({
              type: 'failure',
              data: null,
              message: utils.getFormErrorMessage(err)
            })
          } else {
            const params = {
              ...this.getFormItemsValue(this.formItems),
              ...utils.formatFormValues(values, this.formItems),
              ...this.mergeFormItemsParams(this.formItems)
            }
            resolve({
              type: 'success',
              data: params,
              message: ''
            })
          }
        })
      })
    }
  },
  render (h) {
    return (
      <a-form form={this.form}>
        <a-row>
          {
            this.formItems && this.formItems.map((formItem) => {
              if (this.isCanShow(formItem)) {
                return (
                  <a-col span={formItem.layout ? formItem.layout.span : 8}>
                    <a-form-item
                      label-col={{ span: formItem.layout ? formItem.layout.label : 6 }}
                      wrapper-col={{ span: formItem.layout ? formItem.layout.wrapper : 16 }}
                    >
                      {[
                        this.labelRender(h, utils.clone(formItem)),
                        this.wrapperRender(h, utils.clone(formItem))
                      ]}
                    </a-form-item>
                  </a-col>
                )
              } else {
                return ''
              }
            })
          }
        </a-row>
      </a-form>
    )
  }
}
</script>

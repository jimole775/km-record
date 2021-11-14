<script>
import utils from '@/utils'
export default {
  name: 'ApprovalOperation',
  props: {
    operationItem: {
      type: Object,
      default: () => ({})
    },
    bridge: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      approvalResult: '1',
      form: this.$form.createForm(this)
    }
  },
  methods: {
    changeEventForRadios ({ target: { value } }) {
      this.form = this.$form.createForm(this)
      if (this.operationItem.radios) {
        this.operationItem.radios.forEach((radioItem) => {
          if (Number.parseInt(value) === Number.parseInt(radioItem.value)) {
            if (radioItem.event && utils.isFunction(radioItem.event)) {
              radioItem.event(value, this.operationItem, this)
            }
          }
        })
      }
    },
    changeEventForInput (val, option, inputItem) {
      let pureval = ''
      if (val.target) {
        pureval = val.target.value
      } else {
        pureval = val
      }
      if (inputItem.change && utils.isFunction(inputItem.change)) {
        inputItem.change(pureval, this.operationItem, this)
      }
    },
    async emitSubmit () {
      const res = await this.getFieldsValue()
      if (res.type === 'failure') {
        this.$modal.warning({
          title: '提示',
          content: res.message
        })
      } else {
        this.$emit('submit', res.data)
      }
    },
    getFieldsValue () {
      return new Promise((resolve) => {
        this.form.validateFields((err, values) => {
          if (err) {
            resolve({
              type: 'failure',
              data: null,
              message: utils.getFormErrorMessage(err)
            })
          } else {
            resolve({
              type: 'success',
              data: {
                approvalResult: this.approvalResult,
                ...utils.formatFormValues(values, this.operationItem.inputs)
              },
              message: ''
            })
          }
        })
      })
    }
  },
  render (h) {
    const radionodes = buildRadios.call(this, h)
    const inputnodes = buildInputs.call(this, h)
    const footernodes = buildFooter.call(this, h)
    return (
      <div>
        <a-form form={this.form}>
          <a-row>
            <a-col span={24}>
              {
                radionodes
              }
            </a-col>
            {
              inputnodes
            }
            <a-col span={24}>
              {
                footernodes
              }
            </a-col>
          </a-row>
        </a-form>
      </div>
    )
  }
}

function buildRadios (h) {
  if (this.operationItem.radios) {
    return (
      <a-form-item
        label={'审批'}
        label-col={{ span: 2 }}
        wrapper-col={{ span: 18 }}
      >
        <a-radio-group name="radioGroup" v-model={this.approvalResult} onChange={this.changeEventForRadios}>
          {
            this.operationItem.radios.map((radioItem) => {
              return (
                <a-radio value={radioItem.value}>
                  <span>{ radioItem.label }</span>
                  {
                    radioItem.title &&
                    <a-tooltip title={radioItem.title}>
                      <a-icon type="question-circle-o" />
                    </a-tooltip>
                  }
                </a-radio>
              )
            })
          }
        </a-radio-group>
      </a-form-item>
    )
  } else {
    return ''
  }
}

function buildInputs (h) {
  if (this.operationItem.inputs) {
    return this.operationItem.inputs.map((inputItem, index) => {
      if (inputItem.permissions.includes(this.approvalResult)) {
        return (
          <a-col span={inputItem.layout ? inputItem.layout.span : 8}>
            <a-form-item
              label-col={{ span: inputItem.layout ? inputItem.layout.label : 6 }}
              wrapper-col={{ span: inputItem.layout ? inputItem.layout.wrapper : 16 }}
            >
              {[
                labelRender.apply(this, [h, inputItem, index]),
                wrapperRender.apply(this, [h, inputItem, index])
              ]}
            </a-form-item>
          </a-col>
        )
      } else {
        return ''
      }
    })
  } else {
    return ''
  }
}

function labelRender (h, inputItem, index) {
  let labelC = null
  if (inputItem.label) {
    labelC = h('span', { slot: 'label' }, inputItem.label)
  }
  if (inputItem.labelCustomRender) {
    labelC = inputItem.labelCustomRender(h, inputItem, this)
  }
  return labelC
}

function wrapperRender (h, inputItem, index) {
  if (inputItem.wrapperCustomRender) {
    return inputItem.wrapperCustomRender(this.$createElement, inputItem, this)
  } else {
    return (
      <inputItem.component
        key={inputItem.key}
        ref={`${inputItem.key}_${index}`}
        props={inputItem.props}
        attrs={inputItem.attrs}
        domProps={inputItem.domProps}
        vDecorator={[inputItem.key, { initialValue: inputItem.default || inputItem.value, rules: [{ required: inputItem.required, message: `请确认${inputItem.label}` }] }]}
        onChange={(val, option) => this.changeEventForInput(val, option, inputItem)}
      />
    )
  }
}

function buildFooter (h) {
  if (this.operationItem.footerCustomRender) {
    return this.operationItem.footerCustomRender(h, this.operationItem, this)
  } else {
    return (
      <a-form-item
        label={' '}
        label-col={{ span: 2 }}
        wrapper-col={{ span: 18 }}
      >
        <a-button type="primary" onClick={this.emitSubmit}>提交</a-button>
      </a-form-item>
    )
  }
}

</script>
<style lang="less" scoped>
.footer {
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

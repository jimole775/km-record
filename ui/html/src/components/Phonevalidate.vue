<script>
import { getToken } from '@/utils/auth'
import api from '@/api'
import utils from '@/utils'
export default {
  props: {
    vtype: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      modal: {
        show: false,
        title: '',
        content: '',
        userPhone: ''
      },
      xToken: getToken(),
      countdown: null,
      verifyFailMessage: false,
      form: this.$form.createForm(this)
    }
  },
  methods: {
    async validate (apipost, params) {
      const response = apipost && await apipost(params)
      const result = await this.needvalidate(response)
      if (result) {
        // 需要校验(供应商不需要校验)
        // {"code":50001,"message":"{title: '', content: 未完成二次授权, phone: 136*****888}","data":null}
        // {"code":50002,"message":"{title: '', content: 二次授权验证码错误, phone: 136*****888}","data":null}
        // {"code":50003,"message":"{title: '', content: 二次授权验证码过期, phone: 136*****888}","data":null}
        const { title, content, phone } = result
        this.modal.title = title
        this.modal.content = content
        this.modal.userPhone = phone
        this.showVerifyModal()
      } else {
        return Promise.resolve(response)
      }
    },
    countting () {
      this.countdown -= 1
      setTimeout(() => {
        if (this.countdown > 0) return this.countting()
      }, 1000)
    },
    async getCode () {
      this.countdown = 60
      this.countting()
      this.cearFailMessage()
      const res = await api.getDoubleCheckVerifyCode()
      // code: 50004
      // data: null
      // message: "手机号不正确，请联系管理员"
      if (res.code === 50004) {
        this.$message.warning(res.message || '请求失败，请联系管理员')
      }
    },
    /**
     * @param {Object} res 这里有可能是axios对象，也有可能是业务对象
     *                     axios对象会有headers信息
     */
    async needvalidate (response) {
      try {
        this.cearFailMessage()
        let result = null
        // 如果返回的是有可能是axios对象，也有可能是业务对象
        let responsedata = response
        let businessdata = {}
        if (utils.isAxiosResponse(response)) {
          responsedata = response.data
        }
        if (utils.isBlob(responsedata)) {
          // 转成文件流，主要为了兼容下载接口
          const blob = new Blob([responsedata], { type: 'application/octet-stream' })
          const restext = await utils.readBlobAsText(blob)
          businessdata = JSON.parse(restext)
        }
        if (utils.isObject(responsedata)) {
          businessdata = responsedata
        }
        if (/\b5000\d\b/g.test(businessdata.code)) {
          const msgstr = businessdata.message
          result = JSON.parse(msgstr)
        }
        return Promise.resolve(result)
      } catch (error) {
        return Promise.resolve(null)
      }
    },
    showVerifyModal () {
      this.modal.show = true
      this.cearFailMessage()
    },
    hideVerifyModal () {
      this.modal.show = false
      this.cearFailMessage()
      this.form.resetFields()
    },
    cearFailMessage () {
      this.verifyFailMessage = ''
    },
    verifies () {
      // GET /api/permission/doubleCheck
      // 参数: verifyCode=验证码
      // 正常 200, "二次授权验证成功"
      // 50002, "二次授权验证码错误"
      // 50003, "二次授权验证码过期"
      this.form.validateFields(async (error, values) => {
        if (error) {
          return
        }
        const res = await api.doExportDoubleCheck(values.code, this.$props.vtype)
        if (res.code === 200) {
          this.$message.success(res.message || '授权成功')
          this.hideVerifyModal()
        } else {
          this.verifyFailMessage = res.message || '授权失败'
        }
      })
    }
  },
  render (h) {
    return (
      <a-modal
        v-model={this.modal.show}
        title={this.modal.title}
        width="50%"
        mask-closable={false}
      >
        <div slot="footer">
          <a-button key="back" onClick={this.hideVerifyModal}>取消</a-button>
          <a-button
            type="primary"
            onClick={this.verifies}
          >
            验证
          </a-button>
        </div>
        <h3 align="center">{this.modal.content}</h3>
        <a-form form={this.form}>
          <a-row>
            <a-col span={16}>
              <a-form-item
                label="短信验证码"
                label-col={{ span: 15 }}
                wrapper-col={{ span: 9 }}
              >
                <a-input
                  placeholder="请输入验证码"
                  v-decorator={['code', { rules: [{ required: true, message: '请输入正确的验证码' }] }]}
                />
              </a-form-item>
            </a-col>
            <a-col span={6}>
              <a-form-item
                label=" "
                label-col={{ span: 6 }}
                wrapper-col={{ span: 18 }}
              >
                {this.countdown === null && <a-button onClick={ this.getCode }>点击获取</a-button>}
                {this.countdown === 0 && <a-button onClick={ this.getCode }>重新获取</a-button>}
                {this.countdown > 0 && <a-button disabled>{ this.countdown }s</a-button>}
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
        <h4 align="center">（请在 { this.modal.userPhone || '' } 手机号中查收验证码短信）</h4>
        {this.verifyFailMessage && <h4 align="center" style="color: red">验证码校验不通过，请重新验证</h4>}
      </a-modal>
    )
  }
}
</script>

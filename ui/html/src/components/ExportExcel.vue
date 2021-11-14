<template>
  <div style="display: inline">
    <a-tooltip>
      <template slot="title">
        导出
      </template>
      <a-button class="cir-button button-export" @click="sniffExports" />
    </a-tooltip>
    <Phonevalidate ref="PhonevalidateRef" />
  </div>
</template>
<script>
import Vue from 'vue'
import api from '@/api'
import utils from '@/utils'
import { mapActions } from 'vuex'
import { getToken } from '@/utils/auth'
import Phonevalidate from '@/components/Phonevalidate'
export default {
  name: 'ExportExcel',
  components: {
    Phonevalidate
  },
  props: {
    type: {
      type: String, // default | permission
      default: 'default'
    },
    api: {
      type: String,
      default: ''
    },
    params: {
      type: Object | Function,
      default: () => ({})
    },
    validate: {
      type: Function,
      default: () => true
    },
    fileName: {
      type: String,
      default: '导出文件'
    }
  },
  data () {
    return {
      xToken: getToken()
    }
  },
  computed: {
    userRole () {
      return this.$store.state.global.userRole
    }
  },
  methods: {
    ...mapActions(['pushExportingList']),
    getTrulyParams () {
      let res = {}
      if (utils.isObject(this.params)) {
        res = utils.clone(this.params)
      }
      if (utils.isFunction(this.params)) {
        res = this.params()
      }
      return res
    },
    async jsonHandler (res) {
      let backendData = res
      if (backendData.code === 200) {
        // 'async' 是异步下载类型
        if (backendData.data && backendData.data.type === 'async') {
          this.pushExportingList({ fileName: this.fileName, fileKey: backendData.data.fileKey })
        } else {
          // 非异步下载类型，当前还没有使用这个接口类型
        }
      } else {
        this.$message.warning(backendData.message)
      }
    },
    async sniffExports () {
      const pass = this.validate()
      if (!pass) return false
      let res = null
      Vue.bus.emit('loading', true)
      const apiFun = api[this.api]
      if (utils.isFunction(apiFun)) {
        if (this.type === 'permission') {
          res = await this.$refs.PhonevalidateRef.validate(apiFun, this.getTrulyParams())
        } else {
          res = await apiFun(this.getTrulyParams())
        }
        Vue.bus.emit('loading', false)
      } else {
        Vue.bus.emit('loading', false)
        this.$message.error('ExportExcel => 请先在api对象中设置好接口！')
      }
      if (utils.isBackendResponse(res)) {
        this.jsonHandler(res)
      }
      if (utils.isAxiosResponse(res)) {
        this.axiosHandler(res)
      }
    },
    async axiosHandler (res) {
      if (utils.isBlob(res.data)) {
        const responseData = await utils.readBlobAsText(res.data)
        if (utils.isBackendResponse(responseData)) {
          this.jsonHandler(responseData)
        } else {
          utils.blobToURI(res)
        }
      } else if (utils.isString(res.data)) {
        if (utils.isJSONString(res.data)) {
          this.jsonHandler(JSON.parse(res.data))
        } else {
          throw new Error('未知的返回类型')
        }
      } else if (utils.isObject(res.data)) {
        if (utils.isBackendResponse(res.data)) {
          this.jsonHandler(res.data)
        } else {
          throw new Error('未知的返回类型')
        }
      }
    }
  }
}
</script>

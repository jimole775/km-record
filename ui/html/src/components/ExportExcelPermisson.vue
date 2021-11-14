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
import axios from 'axios'
import utils from '@/utils'
import { mapActions } from 'vuex'
import { getToken } from '@/utils/auth'
import Phonevalidate from '@/components/Phonevalidate'
export default {
  name: 'ExportExcelPermission',
  components: {
    Phonevalidate
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    api: {
      type: String,
      default: ''
    },
    params: {
      type: Object,
      default: null
    },
    fileName: {
      type: String,
      default: 'excel'
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
    downloadHandler (res) {
      Vue.bus.emit('loading', true)
      try {
        // 转成文件流，主要为了兼容下载接口
        const blob = new Blob([res.data], { type: 'application/octet-stream' })
        // 无需校验，直接下载文件
        const link = document.createElement('a')
        const fileName = decodeURI(res.headers['content-disposition'].split(';')[1].split('=')[1])
        link.style.display = 'none'
        link.href = URL.createObjectURL(blob)
        link.setAttribute('download', fileName)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } catch (error) {
        this.$modal.error({
          title: '导出失败',
          content: error.toString()
        })
      }
      Vue.bus.emit('loading', false)
    },
    async sniffExports () {
      Vue.bus.emit('loading', true)
      this.$refs.PhonevalidateRef.validate(axios, {
        method: 'post',
        url: this.api,
        data: this.params,
        responseType: 'blob',
        headers: { 'x-token': getToken() }
      }).then(async (res) => {
        Vue.bus.emit('loading', false)
        if (!res) return
        // 兼容mock工具在dev环境对数据的重构
        if (process.env.NODE_ENV === 'development') {
          if (res.data && res.data.data && res.data.data.type === 'async') {
            this.pushExportingList({ fileName: this.fileName, fileKey: res.data.data.fileKey })
          } else {
            this.downloadHandler(res)
          }
        } else {
          if (res.data && utils.isBlob(res.data) && res.data.type === 'application/json') {
            let backendData = await utils.readBlobAsText(res.data)
            // 把字符串转成JSON data
            if (utils.isJSONString(backendData)) {
              backendData = JSON.parse(backendData)
            }
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
          } else {
            this.downloadHandler(res)
          }
        }
      })
    }
  }
}
</script>

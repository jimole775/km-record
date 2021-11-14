<template>
  <div class="uploader-base">
    <a-upload
      name="file"
      :multiple="multiple"
      :accept="supportSeries"
      :before-upload="beforeUploadEvent"
      :file-list="fileList"
      :show-upload-list="false"
      @preview="downloadFile"
    >
      <a-button
        ghost
        type="primary"
        :disabled="disabled"
      >
        <a-icon type="upload" /> {{ text }}
      </a-button>
    </a-upload>
    <template v-for="(fileItem, index) in fileDataStore">
      <div class="download-bar" :key="index">
        <a-icon class="file-icon" type="paper-clip" />
        <SDownload class="file-content" :value="fileItem" />
        <a class="file-close" @click="() => remove(fileItem)">x</a>
      </div>
    </template>
  </div>
</template>

<script>
import api from '@/api'
import Vue from 'vue'
import utils from '@/utils'
import { getToken } from '@/utils/auth'

export default {
  name: 'SUpload',
  props: {
    injectParams: {
      type: Object,
      default: null
    },
    action: {
      type: String,
      default: 'gfsfileupload'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    value: {
      type: Array,
      default: () => []
    },
    multiple: {
      type: Boolean,
      default: false
    },
    accept: {
      type: String,
      default: ''
    },
    text: {
      type: String,
      default: '上传文件'
    }
  },
  data () {
    return {
      fileList: [],
      fileDataStore: []
    }
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  computed: {
    supportSeries () {
      return this.accept ? this.accept : this.$store.getters.getFileTypePermisson()
    }
  },
  watch: {
    value: {
      handler (val) {
        // v-model 绑定的对象被清空时，对应的数据也需要清空
        if (!val) {
          this.fileDataStore = []
          this.fileList = []
        } else {
          this.fileDataStore = val
          this.fileList = []
        }
      },
      immediate: true
    }
  },
  methods: {
    // 下载附件
    downloadFile (file) {
      this.fileDataStore.forEach((item) => {
        if (file.name === item.fileName) {
          api.gfsfiledownload(item.fileId)
        }
      })
    },
    // 移除文件
    remove (file) {
      for (let index = 0; index < this.fileDataStore.length; index++) {
        const item = this.fileDataStore[index]
        if (file.fileId === item.fileId) {
          this.fileList.splice(index, 1)
          this.fileDataStore.splice(index, 1)
          break
        }
      }
      this.$emit('change', this.fileDataStore)
    },
    // 上传文件，并存储返回的url
    async beforeUploadEvent (file, files) {
      const pass = utils.verifyUploadType(file.name, this.supportSeries)
      if (pass) {
        Vue.bus.emit('loading', true) // 显示正在上传
        Vue.bus.emit('uploadDisabled', true) // 提交按钮禁用
        const form = this.extendsForm(file)
        api[this.action](form).then((res) => this.successHandler(res, file), this.failerHandler)
      }
      return false
    },
    successHandler (res, file) {
      Vue.bus.emit('uploadDisabled', false)
      Vue.bus.emit('loading', false)
      if (res.data === null || res.data === undefined) {
        res.message && this.$modal.warning({
          title: '提示',
          content: res.message
        })
        return false
      }
      if (utils.isString(res.data)) {
        this.$message.warning(
          `文件上传失败 ${
            res.data.split(':')[res.data.split(':').length - 1]
          }`
        )
        this.$emit('change', this.fileDataStore)
      }
      if (utils.isObject(res.data)) {
        this.fileDataStore.push(res.data)
        this.fileList.push(file)
        this.$message.success('文件上传成功')
        this.$emit('change', this.fileDataStore, this.fileList)
      }
    },
    failerHandler (res) {
      Vue.bus.emit('uploadDisabled', false)
      Vue.bus.emit('loading', false)
      this.$modal.error({ title: '上传失败', content: res.message })
    },
    extendsForm (file) {
      const form = new FormData()
      form.append('file', file)
      form.append('auth_token', `oms:${getToken()}`)
      form.append('scene', `oms`)
      form.append('output', 'json')
      if (this.injectParams) {
        Object.keys(this.injectParams).forEach((key) => {
          form.append(key, this.injectParams[key])
        })
      }
      return form
    }
  }
}
</script>
<style lang="less" scoped>
.file-icon {
  font-size: 14px;
  left: 0.4rem;
  top: 0.4rem;
  position: absolute;
  color: rgba(0, 0, 0, 0.45);
}
.file-content {
  font-size: 14px;
  text-indent: 1.5rem;
}
.file-close {
  position: absolute;
  right: 1rem;
  top: -1px;
  color: #ff4545;
  padding: 0 0.3rem;
  font-size: 13px;
  &:hover {
    background-color: #efefef;
  }
}

.download-bar {
  line-height: 1.5rem;
  position: relative;
  /deep/ .default-style {
    margin: 0;
    line-height: 1.5rem;
    &:hover {
      background-color: #efefef;
    }
  }
}

.uploader-base {
  transition: height 0.3s;
}
</style>

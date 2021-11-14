<template>
  <div class="default-style">
    <a-tooltip v-if="len" :title="fileData.fileName">
      <a class="href-style" @click="download">{{ fileData.fileName | ellipsisSentence(len) }}</a>
    </a-tooltip>
    <a v-else class="href-style" @click="download">{{ fileData.fileName }}</a>
    &nbsp;
    <a
      v-if="fileData.fileName && canPerview"
      title="预览"
      class="preview-style"
      @click="getFilePreviewUrl"
    >
      <a-icon type="eye" />
    </a>
    <PreviewFrame :modal="modal" />
  </div>
</template>
<script>
import utils from '@/utils'
import PreviewFrame from '@/components/PreviewFrame'
import api from '@/api'
const imgSeries = /\.(jpe?g|png|bmp|gif|tiff|webp)$/i
const docSeries = /\.(xlsx?|docx?|pdf|pptx?)$/i
export default {
  name: 'SDownload',
  components: { PreviewFrame },
  props: {
    value: {
      type: Object,
      default: () => ({})
    },
    len: {
      type: Number,
      default: 0
    }
  },
  watch: {
    fileData: {
      handler (val) {
        if (val) {
          this.modal.name = val['fileName'] || ''
          if (docSeries.test(this.modal.name)) {
            this.modal.type = 'doc'
          }
          if (imgSeries.test(this.modal.name)) {
            this.modal.type = 'img'
          }
        }
      },
      deep: true,
      immediate: true
    }
  },
  computed: {
    canPerview () {
      return docSeries.test(this.fileData.fileName)
    }
  },
  filters: {
    ellipsisSentence: utils.ellipsisSentence.bind(utils)
  },
  data () {
    return {
      modal: {
        show: false,
        data: '',
        type: '',
        name: ''
      },
      fileData: this.value
    }
  },
  methods: {
    download () {
      if (this.fileData['fileId']) {
        api.gfsfiledownload(this.fileData['fileId'])
      }
    },
    async getFilePreviewUrl () {
      const res = await api.getFilePreviewUrl(this.fileData)
      if (res.code === 200) {
        this.modal.data = res.data
        this.modal.show = true
      } else {
        this.modal.show = false
        this.$message.error('预览失败')
      }
    }
  }
}
</script>
<style lang="less" scoped>
.default-style {
  line-height: 1.5;
  margin-top: 0.5rem;
  word-break: break-word;
  a.href-style {
    color: #2DC84D;
    text-decoration: underline;
  }
  a.preview-style {
    color: #868C97;
  }
}
</style>

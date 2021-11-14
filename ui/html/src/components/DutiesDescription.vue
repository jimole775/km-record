<template>
  <a-modal
    v-model="modal.show"
    :width="modalWidth"
    :title="htmlTitle"
    :footer="false"
  >
    <div v-if="htmlContent" v-html="htmlContent" />
  </a-modal>
</template>
<script>
import api from '@/api'
export default {
  props: {
    modal: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      modalWidth: '600pt',
      htmlTitle: '',
      htmlContent: ''
    }
  },
  watch: {
    modal: {
      async handler (val) {
        if (val.show && !this.htmlContent) {
          const res = await api.getrequirementservicesdocumentquery(1)
          if (res.code === 200) {
            this.htmlTitle = res.data.name
            this.htmlContent = res.data.value
            this.modalWidth = this.getTableWidth(this.htmlContent)
          } else {
            this.$modal.warning({
              title: '提示',
              content: res.message
            })
          }
        } else {
          // 清空为了避免htmlContent中内嵌的公共style会影响其他同名样式
          this.htmlTitle = ''
          this.htmlContent = ''
        }
      },
      deep: true
    }
  },
  methods: {
    getTableWidth (htmlString = '') {
      let tableFirstTag = htmlString.match(/<table.*?>/)
      tableFirstTag = tableFirstTag ? tableFirstTag[0] : ''
      let style = tableFirstTag.match(/\bstyle=.*?width:.*?;/)
      style = style ? style[0] : ''
      let width = style.replace(/\bstyle=.*?width:(\d+\.*\d*)(\w+);/, '$1')
      let unit = style.replace(/\bstyle=.*?width:(\d+\.*\d*)(\w+);/, '$2')
      return (Number.parseFloat(width || 600) + 22) + unit
    }
  }
}
</script>
<style lang="less" scoped>
</style>

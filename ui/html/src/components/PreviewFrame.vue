<template>
  <a-modal
    v-model="modal.show"
    width="80%"
    style="top: 4rem"
    :closable="false"
    :footer="null"
  >
    <iframe
      v-if="modal.type === 'doc'"
      class="iframe"
      :src="modal.data"
      :style="{ height: this.height }"
    />
    <img
      v-else-if="modal.type === 'img'"
      class="iframe"
      :src="modal.data"
      :style="{ height: this.height }"
    />
    <div v-else>不支持的文件类型！</div>
  </a-modal>
</template>
<script>
export default {
  name: 'PreviewFrame',
  props: {
    modal: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    const win = document.body
    return {
      height: (win.clientHeight * 0.8) + 'px'
    }
  }
}
</script>
<style lang="less" scoped>
.iframe {
  border: 1px;
  width: 100%;
}
</style>

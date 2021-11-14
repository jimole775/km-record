<template>
  <a-upload
    name="file"
    accept=".xls, .xlsx"
    :before-upload="beforeUpload"
    :file-list="fileList"
    class="import-table"
  >
    <a-tooltip>
      <template slot="title">导入</template>
      <a-button
        class="cir-button button-import"
      />
    </a-tooltip>
  </a-upload>
</template>

<script>
import utils from '@/utils'
import api from '@/api'
export default {
  name: 'Importer',
  props: {
    api: {
      type: String
    }
  },
  data () {
    return {
      fileList: []
    }
  },
  computed: {
    supportSeries () {
      const dicts = this.$store.getters.getDictByGroupCode('upload_file_suffix_while_list')
      const supports = dicts.map((item) => {
        return '.' + item.itemCode
      })
      return this.accept ? this.accept : supports.join(',')
    }
  },
  methods: {
    number2money: utils.number2money,
    money2number: utils.money2number,
    getApiFunction (apiNameOrFunction) {
      if (utils.isFunction(apiNameOrFunction)) {
        return apiNameOrFunction
      }
      if (utils.isString(apiNameOrFunction)) {
        return api[apiNameOrFunction] || function () {}
      }
      if (utils.isUndefined(apiNameOrFunction)) {
        return function () {}
      }
    },
    // 导入
    async beforeUpload (file) {
      const pass = utils.verifyUploadType(file.name, this.supportSeries)
      if (!pass) return false
      if (!this.api) return false
      const params = new FormData()
      params.append('file', file)
      const res = await this.getApiFunction(this.api)(params)
      if (res.code === 200) {
        this.$message.success('导入成功')
        // this.fetchData()
        this.$emit('update', res.data)
      } else {
        this.$modal.warning({
          title: '提示',
          okText: '确定',
          content: res.message
        })
      }
      return false
    }
  }
}
</script>

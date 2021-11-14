<template>
  <Panel :code="code" title="导入样例" :description="description">
    <template slot="example">
      <div class="moveBox">
        <Importer style="padding: 0 1rem" :api="'postdatamodifyimportRepairSignInfoExcel'" @update="getImportData" />
        <a-tooltip style="padding: 0 1rem">
          <template slot="title">导入模板下载</template>
          <a-button
            @click="downLoadTemplate"
            class="cir-button button-import-template-down"
          />
        </a-tooltip>
      </div>
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import description from './description.md'
import Importer from '@/components/Importer'
import utils from '@/utils'
export default {
  title: '导入样例',
  name: 'Example1',
  components: {
    Importer
  },
  data () {
    return {
      code,
      description
    }
  },
  methods: {
    // 导入模板下载
    downLoadTemplate () {
      utils.exportGetFile('/api/files/temple?fileName=模板.xlsx')
    },
    getImportData (data) {
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify(data)
      })
    }
  }
}
</script>

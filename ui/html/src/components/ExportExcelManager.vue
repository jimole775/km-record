<template>
  <div>
    <div v-if="(exportingList && exportingList.length) || failureList.data.length" class="export-hover-button">
      <a-tooltip v-model="tipmodal.show" trigger="contextmenu">
        <template slot="title">
          <span>{{ tipmodal.message }}</span>
        </template>
        <a-button @click="managermodal.show = true">
          <span><a-icon type="download" />&nbsp;<span class="desc">导出列表</span></span>
        </a-button>
      </a-tooltip>
    </div>
    <a-modal
      class="export-hover-window"
      title="导出列表"
      :footer="null"
      v-model="managermodal.show"
    >
      <a-list bordered :data-source="exportingList">
        <a-list-item slot="renderItem" slot-scope="item">
          <div class="list-item">
            <a-button class="fake-loading-icon" :loading="true" :title="'计算导出中...'" />
            <span class="file-name">{{ item.fileName }}</span>
            <a-button class="close-icon" @click="() => delExportListItemConfirm(item)"><a-icon type="close" /></a-button>
          </div>
        </a-list-item>
      </a-list>
      <a-list v-if="failureList.data.length" bordered :data-source="failureList.data">
        <a-list-item slot="renderItem" slot-scope="item, index">
          <div class="list-item">
            <a-tooltip>
              <template slot="title">
                <span>导出失败，请联系管理员！</span>
              </template>
              <a-button class="fake-loading-icon" @click="() => tryReloadFormErrorList(item, index)"><a-icon type="exclamation-circle" /></a-button>
            </a-tooltip>
            <span class="file-name">{{ item.fileName }}</span>
            <a-button class="close-icon" @click="() => delErrorListItem(item)"><a-icon type="close" /></a-button>
          </div>
        </a-list-item>
      </a-list>
    </a-modal>
  </div>
</template>
<script>
import api from '@/api'
import utils from '@/utils'
import { mapActions } from 'vuex'
export default {
  name: 'ExportExcelManager',
  data () {
    return {
      managermodal: {
        show: false
      },
      heartbeatState: {
        timesign: null
      },
      exportingListBackup: [], // 用来备份对比data的，已方便判断data有没有新增
      failureList: {
        data: [],
        backup: []
      },
      tipmodal: {
        message: '',
        normal: '已加入导出队列，可点击查看！',
        failure: '导出失败，可点击查看！',
        success: '导出成功！',
        duplicate: '已在队列中！',
        show: false,
        timesign: null
      }
    }
  },
  watch: {
    'exportingList': {
      handler (data = []) {
        const backup = this.exportingListBackup || []
        // const duplicateItem = this.hasDuplicate(data)
        // if (duplicateItem) {
        // this.showDuplicateTips(duplicateItem)
        // return this.delExportListItem(duplicateItem)
        // }
        if (data.length !== backup.length) {
          this.showNormalTips()
          this.heartbeat()
          this.syncModalDataBak()
        }
      },
      immediate: true
    },
    'failureList.data': {
      handler (data = []) {
        const backup = this.failureList.backup || []
        if (data.length !== backup.length) {
          this.showFailureTips()
          this.syncModalDataBak()
        }
      },
      immediate: true
    }
  },
  computed: {
    exportingList () {
      const cache = this.$store.getters.getExportingList
      if (cache && cache.length) {
        return cache
      } else {
        return this.$store.state.global.exportingList
      }
    }
  },
  methods: {
    ...mapActions(['pushExportingList', 'spliceExportingList']),
    delExportListItemConfirm (item) {
      this.$modal.confirm({
        title: '提示',
        content: '文件正在导出中，是否删除这个任务？',
        okText: '是',
        cancelText: '否',
        onOk: () => {
          this.delExportListItem(item)
        }
      })
    },
    hasDuplicate (data = []) {
      let res = null
      for (let i = 0; i < data.length; i++) {
        const go = data[i]
        for (let j = data.length - 1; j > i; j--) {
          const back = data[j]
          if (go.fileName === back.fileName && j !== i) {
            res = back
            break
          }
        }
      }
      return res
    },
    showFailureTips (item = { fileName: '' }) {
      const data = this.failureList.data || []
      const backup = this.failureList.backup || []
      if (data.length > backup.length) {
        this.tipmodal.message = `${item.fileName}${this.tipmodal.failure}`
        this.showTipsHandler()
      }
    },
    showNormalTips (item = { fileName: '' }) {
      const data = this.exportingList || []
      const backup = this.exportingListBackup || []
      if (data.length > backup.length) {
        this.tipmodal.message = `${item.fileName}${this.tipmodal.normal}`
        this.showTipsHandler()
      }
    },
    showSuccessTips (item = { fileName: '' }) {
      this.tipmodal.message = `${item.fileName}${this.tipmodal.success}`
      this.$message.success(this.tipmodal.message)
    },
    showDuplicateTips (item = { fileName: '' }) {
      this.tipmodal.message = `${item.fileName}${this.tipmodal.duplicate}`
      this.$message.success(this.tipmodal.message)
    },
    showTipsHandler () {
      clearTimeout(this.tipmodal.timesign)
      this.tipmodal.timesign = null
      this.tipmodal.show = true
      this.tipmodal.timesign = setTimeout(() => {
        this.tipmodal.show = false
      }, 2000)
    },
    heartbeat () {
      clearTimeout(this.heartbeatState.timesign)
      this.heartbeatState.timesign = null
      this.heartbeatState.timesign = setTimeout(() => {
        if (this.exportingList && this.exportingList.length) {
          this.heartbeatQueueHandler().then(() => {
            return this.heartbeat()
          })
        }
      }, 1000)
    },
    addExportItem (item) {
      this.pushExportingList(item)
    },
    addErrorItem (item) {
      this.failureList.data.push(item)
    },
    delExportListItem (item) {
      for (let i = 0; i < this.exportingList.length; i++) {
        const loopItem = this.exportingList[i]
        if (loopItem.fileName === item.fileName) {
          this.spliceExportingList(i)
          break
        }
      }
    },
    delErrorListItem (item) {
      for (let i = 0; i < this.failureList.data.length; i++) {
        const loopItem = this.failureList.data[i]
        if (loopItem.fileName === item.fileName) {
          this.failureList.data.splice(i, 1)
          break
        }
      }
    },
    heartbeatQueueHandler () {
      return new Promise((resolve, reject) => {
        const exportingList = utils.clone(this.exportingList)
        exportingList.forEach(async (item, index) => {
          const res = await api.getDownFileFileKey(item).catch(() => {})
          if (res && res.code === 200) {
            if (res.data && utils.isValuable(res.data.fileStatus)) {
              // const statusmap = {
              //   '-1': '不存在',
              //   0: '失败',
              //   1: '成功',
              //   2: '处理中'
              // }
              if (res.data.fileStatus === -1 || res.data.fileStatus === 0) {
                this.addErrorItem(item)
                this.delExportListItem(item)
              }
              if (res.data.fileStatus === 1) {
                this.showSuccessTips(item)
                this.delExportListItem(item)
                this.downloadHandler(res, item)
              }
            } else {
              this.addErrorItem(item)
              this.delExportListItem(item)
            }
          } else {
            this.addErrorItem(item)
            this.delExportListItem(item)
          }
          if (index + 1 === exportingList.length) {
            resolve()
          }
        })
      })
    },
    tryReloadFormErrorList (item, index) {
      this.pushExportingList(item)
      this.delErrorListItem(item)
    },
    syncModalDataBak () {
      this.exportingListBackup = [].concat(this.exportingList)
      this.failureList.backup = [].concat(this.failureList.data)
    },
    downloadHandler (res, item) {
      const link = res.data && res.data.fileUrl
      utils.downloadFileByLink(link, item.fileName)
    }
  }
}
</script>
<style lang="less" scoped>
div.ant-list-item {
  padding-right: 12px;
  padding-left: 12px;
}
span.file-name {
  padding-left: 1rem;
  line-height: 32px;
}
div.list-item {
  position: relative;
  width: 100%;
}
button.close-icon {
  border: 0;
  box-shadow: none;
  color: red;
  position: absolute;
  right: 0;
  top: 0;
}
button.fake-loading-icon {
  padding: 0 0.5rem !important;
  margin: 0 !important;
  border: 0 !important;
  background: none !important;
  box-shadow: none !important;
  cursor: default !important;
  svg {
    color: red;
  }
}
.export-hover-button {
  // position: fixed;
  // right: 150px;
  // bottom: 150px;
  border: 0;
  // width: 52px;
  // height: 52px;
  // overflow: hidden;
  // -webkit-box-shadow: 0 2px 4px 0 rgba(0,0,0,.2);
  // box-shadow: 0 2px 4px 0 rgba(0,0,0,.2);
  // border-radius: 26px;
  text-align: center;
  // line-height: 52px;
  // -webkit-transition: all .3s ease-in-out;
  // transition: all .3s ease-in-out;
  /deep/button.ant-btn {
    width: 100%;
    height: 100%;
    border: 0;
    // border-radius: 100%;
    background: none;
    color: #2dc84d;
    /deep/i.anticon {
      font-size: 1.3rem;
    }
    span.desc {
      font-size: 0.8rem;
      position: relative;
      top: -1px;
    }
  }
}
</style>

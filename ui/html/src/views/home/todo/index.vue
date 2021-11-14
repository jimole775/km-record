<template>
  <div>
    <div style="padding: 0">
      <a-tabs
        hide-add
        type="editable-card"
        v-model="tabActive"
        @change="tabChange"
      >
        <a-tab-pane
          :key="'0'"
          :tab="'公告指南'"
          :closable="false"
        />
      </a-tabs>
    </div>
    <div class="guideNone" v-if="guidesList.length===0">暂无公告</div>
    <div class="guidelistbox">
      <div v-if="guidesList.length>0" class="more-bar">
        <a href="javascript:;" @click="jumpto">更多</a>
      </div>
      <ul>
        <li class="flex flex-jb" v-for="item in guidesList" :key="item.id">
          <p style="margin-bottom:0" class="flex1 flex contentP flex-ac">
            <a class="item_title" @click="showNotice(item)">
              <span class="item_type">【{{ item.documentTypeName }}】</span>
              <a-tooltip :title="item.documentName">
                <span class="item_text">{{ item.documentName }}</span>
              </a-tooltip>
            </a>
          </p>
          <p style="margin-bottom:0">
            <span>{{ item.publicTime | queryDate }}</span>
          </p>
        </li>
      </ul>
    </div>
    <AutoNoticeModal
      v-if="autoNotices.show"
      :auto-notices="autoNotices"
      @update="getReadSuccess"
    />
    <GuiViewer
      :modal="guiviewmodal"
      @update="getReadSuccess"
    />
  </div>
</template>
<script>
import api from '@/api'
import utils from '@/utils'
import GuiViewer from '@/views/basic-info/gui-manager/modals/GuiViewer.vue'
import AutoNoticeModal from './AutoNoticeModal.vue'
export default {
  name: 'Notices',
  data () {
    return {
      tabActive: '0',
      guidesList: [],
      guiviewmodal: {
        show: false,
        data: {}
      },
      autoNotices: {
        show: false,
        data: {}
      }
    }
  },
  components: {
    GuiViewer,
    AutoNoticeModal
  },
  filters: {
    // 处理时间戳
    queryDate (dateTimp) {
      return utils.date2YMD(dateTimp)
    }
  },
  created () {
    this.getGuiList()
    this.getAutoGuides()
  },
  methods: {
    // 查看系统公告详情
    showNotice (item) {
      this.guiviewmodal.show = true
      this.guiviewmodal.data = item
    },
    tabChange (val) {
      this.tabActive = val
    },
    // 把未读公告以弹窗的形式展示
    async getAutoGuides () {
      this.autoNotices.data = []
      const res = await api.postguideserviceshomenotice()
      if (res.code === 200 && res.data) {
        this.autoNotices.data = res.data
      }
      if (this.autoNotices.data.length > 0) {
        this.autoNotices.show = true
      }
    },
    // 跳转系统公告列表
    jumpto () {
      this.$router.push('manage_guide')
    },
    async getGuiList () {
      const res = await api.postguideservicespage({
        pageNum: 1,
        pageSize: 5,
        status: '已发布'
      })
      if (res.code === 200) {
        this.guidesList = res.data.records || []
      }
    },
    // 查看公告后刷新公告列表
    getReadSuccess () {
      this.getGuiList()
    }
  }
}
</script>
<style lang="less" scoped>
</style>

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
@media screen and ( max-width: 1365px) {
  .contentP {
    max-width:60%;
  }
}
@media screen and (max-width:1470px) {
  .contentP {
    max-width:67%;
  }
}
.guidelistbox {
  padding: 1rem;
}
.guidelistbox ul li {
  list-style: none;
  border-bottom: 1px solid #e8e8e8;
  padding-bottom: 5px;
  margin-bottom: 10px;
  // max-width: 505px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  position: relative;
  padding-right:30px;
  padding-top:10px;
}

.guidelistbox ul {
  padding-inline-start: 0px;
}
.guidelistbox ul li span {
  color: #999999;
  padding-right: 12px;
  padding-left: 5px;
}
.guidelistbox ul li a {
  color: #333333;
}
.guideNone {
  padding-top: 25px;
  text-align: center;
  color: #999999;
}
.flex1{flex:1;}
.flex-jb{justify-content: space-between;}
.flex{
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}
.flex-ac{
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}
.item_title{
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: inline-block;
}
.contentP{
  max-width: 70%;
}
.guide-icon {
  margin-right: 10px;
}
.more-bar {
  text-align: right;padding-right: 0.5rem;
}
.item_type {
  padding: 0 !important;
}
.item_text {
  color: #555 !important;
}
</style>

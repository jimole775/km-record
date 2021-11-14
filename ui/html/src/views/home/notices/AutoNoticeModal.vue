<template>
  <a-modal
    v-if="autoNotices.show"
    v-model="autoNotices.show"
    width="1000px"
    :title="modalTitle"
    :mask-closable="false"
    :footer="null"
    @cancel="handCancel"
  >
    <div class="homenoticeBox" @mousemove="mouseIn" @mouseleave="mouseOut">
      <a-carousel
        ref="homenotice"
        :after-change="onChange"
        arrows
        effect="fade"
      >
        <div
          v-if="autoNotices.data.length>1"
          v-show="hideArrow"
          slot="prevArrow"
          class="custom-slick-arrow"
          style="left: 10px;zIndex: 1"
        >
          <a-icon type="left-circle" />
        </div>
        <div
          v-if="autoNotices.data.length>1"
          v-show="hideArrow"
          slot="nextArrow"
          style="right: 10px"
          class="custom-slick-arrow"
        >
          <a-icon type="right-circle" />
        </div>
        <div class="noticeCont" v-for="(item,index) in autoNotices.data" :key="index">
          <h1>{{ item.documentName }}</h1>
          <div class="noticeCont_nav">
            <span>阅读范围：{{ item.readRoleName }}</span>
            <span>发布日期：{{ item.publicTime | queryDate }}</span>
            <span>作者：{{ item.createdName }}</span>
          </div>
          <div class="noticeCont_warp">
            <div v-html="item.content" />
          </div>
          <div v-if="item.guideFileUrl && item.guideFileUrl.length" class="noticeCont_warp bottom_noticeCont_warp">
            <p>相关附件：</p>
            <p v-for="url in item.guideFileUrl" :key="url">
              <SDownload :value="url">
              <!-- <a :href="spillHref(url)">{{ splitUrl(url).fileName }}</a> -->
            </p>
          </div>
        </div>
      </a-carousel>
    </div>
    <div class="dialogFooter3">
      <a-button @click="closeDialog" type="primary">关闭</a-button>
    </div>
  </a-modal>
</template>
<script>
import api from '@/api'
import utils from '@/utils'
import { getToken } from '@/utils/auth'
export default {
  props: {
    autoNotices: {
      type: Object,
      required: true
    }
  },
  watch: {
    'autoNotices.show': {
      handler (val) {
        if (val) {
          const fItem = this.autoNotices.data[0] || {}
          this.changReadNews(fItem)
        } else {
          this.$emit('update')
        }
      },
      immediate: true
    }
  },
  filters: {
    // 处理时间戳
    queryDate (dateTimp) {
      return utils.date2YMD(dateTimp)
    }
  },
  data () {
    return {
      hideArrow: false,
      modalTitle: '公告指南'
    }
  },
  methods: {
    splitUrl: utils.splitUrl,
    spillHref (path) {
      return `${this.$store.getters.getCurrentDomain()}${utils.encodeFileName(path)}?auth_token=oms:${getToken()}`
    },
    async fetchContent (item) {
      if (item.content && item.content.length) {
        return false
      }
      const id = item ? item.id : ''
      const res = await api.getguideservicesdetail({ id })
      if (res.code === 200) {
        this.recordState(item)
        this.$set(item, 'content', res.data.content)
      } else {
        this.$set(item, 'content', res.messge)
      }
    },
    recordState (item) {
      // 如果已经读取过了，不需要再调用
      if (item.isRead) return false
      api.userNotice({
        noticeId: item.id,
        noticeType: item.noticeType
      }).then(res => {
        if (res.code === 200) {
          item.isRead = true
        }
      })
    },
    closeDialog () {
      this.autoNotices.show = false
      this.$emit('update')
    },
    // 右上角的关闭
    handCancel () {
      this.$emit('update')
    },
    homenoticePre () {
      this.$refs.homenotice.prev()
    },
    homenoticeNext () {
      this.$refs.homenotice.next()
    },
    // 绑定回调
    onChange (currentIndex) {
      this.autoNotices.data.forEach((item, index) => {
        if (index === currentIndex) {
          this.changReadNews(item)
        }
      })
    },
    // 触发调用已读的方法
    async changReadNews (item) {
      this.getModalTitle(item)
      this.fetchContent(item)
    },
    getModalTitle (item) {
      this.modalTitle = item.documentTypeName || '公告指南'
    },
    mouseIn (val) {
      if (val) {
        this.hideArrow = true
      }
    },
    mouseOut () {
      this.hideArrow = false
    }
  }
}
</script>
<style lang="less" scoped>
.noticeCont {
  margin-bottom: 20px;
  padding: 0 20px;
  height: 550px;
  overflow-y: auto;
}
.noticeCont_nav {
  padding-top: 10px;
  border-bottom: 1px solid #e8e8e8;
  text-align: center;
  padding-bottom: 8px;
  color: gray;
  font-size: 12px;
}
.noticeCont_nav span {
  padding-right: 10px;
}
.noticeCont h1 {
  text-align: center;
  font-size: 16px;
  font-weight: bold;
}
.noticeCont_warp {
  padding: 30px;
}
.noticeCont_warp p {
  padding-top: 10px;
  text-indent: 2em;
  line-height: 24px;
  margin-bottom: 0px;
  line-height: 24px;
}
.noticeCont_warp p img {
  margin-left: -2em;
  max-width: 100%;
}
.dialogFooter3 {
  padding-top: 30px;
  text-align: center;
}
.ant-carousel .custom-slick-arrow {
  width: 40px;
  height: 40px;
  font-size: 40px;
}
.ant-carousel .custom-slick-arrow:hover {
  color:#05b570;
}
.ant-carousel .custom-slick-arrow:before {
  display: none;
}
.ant-carousel .slick-dots li.slick-active button {
  width: 24px;
  background: @primary-color !important;
  opacity: 1;
}
.ant-carousel .slick-dots li button {
  background: #333333 !important;
}
.ant-carousel .slick-dots {
  bottom: 0px !important;
}
.homenoticeBox{
  position: relative;
}
.homenoticePre{
  position:absolute;
  left: 0px;
  top: 300px;
  z-index: 10000;
  color: @primary-color;
  font-size: 30px;
  color:gray;
}
.homenoticePre :hover{
  color: #05b570;
}

.homenoticeNext{
  position:absolute;
  right: 0px;
  top: 300px;
  z-index: 10000;
  color: @primary-color;
  font-size: 30px;
  color:gray;

}
.homenoticeNext :hover{
  color: #05b570;
}

.bottom_noticeCont_warp {
  border-top: 1px solid #e8e8e8;
}
</style>

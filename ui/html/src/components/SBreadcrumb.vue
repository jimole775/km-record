<template>
  <div class="pt30">
    <a-breadcrumb class="oms-breadcrumb" separator="/">
      <a-breadcrumb-item href="/">
        <!-- <a-icon type="home" @click="toHome" /> -->
        <a @click="toHome">首页</a>
      </a-breadcrumb-item>
      <a-breadcrumb-item v-for="(item, index) in pathArr" :key="index">
        <span>{{ item.breadcrumbName }}</span>
      </a-breadcrumb-item>
    </a-breadcrumb>
  </div>
</template>

<script>
import utils from '@/utils'

export default {
  name: 'SBreadcrumb',
  data () {
    return {
      pathArr: []
    }
  },
  computed: {
    menus () {
      return this.$store.state.global.menus
    }
  },
  watch: {
    menus () {
      this.getPathArr()
    }
  },
  created () {
    this.getPathArr()
  },
  methods: {
    getPathArr () {
      if (!this.menus || this.menus.length === 0) {
        return
      }
      let arr = utils.findPathDFS(this.menus, this.$router.history.current.path)
      this.pathArr = arr.map((item) => {
        return {
          path: item.path,
          breadcrumbName: item.title
        }
      })
    },
    toHome () {
      this.$router.push({
        path: '/'
      })
    }
  }
}
</script>

<style lang="less" scoped>
.oms-breadcrumb {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 45px;
  line-height: 45px;
  padding: 0 15px;
  > span {
    &:last-child {
      color: #333333;
    }
  }
}
</style>

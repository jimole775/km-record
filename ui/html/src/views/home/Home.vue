<template>
  <SLayout>
    {{ text }}
    <Phonevalidate ref="PhonevalidateRef" vtype="clock" />
  </SLayout>
</template>

<script>
import baseMixins from '@/mixins/baseMixins.js'
import Phonevalidate from '@/components/Phonevalidate.vue'
import SLayout from '@/components/SLayout.vue'
export default {
  name: 'Home',
  mixins: [baseMixins],
  components: {
    SLayout,
    Phonevalidate
  },
  data () {
    return {
      approveList: [],
      applyList: [],
      activeKey: '1',
      exceptionDays: 0
    }
  },
  computed: {
    userRole () {
      return this.$store.state.global.userRole
    },
    user () {
      return this.$store.state.global.user
    },
    userAccount () {
      return this.$store.state.global.user.employeeNumber
    }
  },
  created () {
    // this.text = window.asdfghjkl
  },
  methods: {
    jumpToListPage (item) {
      this.mixin_jumping(item, 'list', this.activeKey === '1' ? 'approve' : 'apply')
    },
    jumpToDetailPage (item) {
      this.mixin_jumping(item, 'detail', this.activeKey === '1' ? 'approve' : 'apply')
    },
    // 获取数据字典项的名称
    getDictName (code) {
      const dictItem = this.$store.getters.getDictItemNameByGroupCode(
        'elastic_type',
        code
      )
      if (dictItem) {
        return dictItem.itemName
      } else {
        return code
      }
    },
    dataCall (data) {
      this.exceptionDays = data
    }
  }
}
</script>

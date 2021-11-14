``` html
<template>
  <div>
    <UserSelect v-model="dataSource.user" />
    <a-button type="primary" @click="submitEvent">提交</a-button>
  </div>
</template>
<script>
import UserSelect from '@/components/UserSelect'
export default {
  components: { UserSelect },
  data () {
    return {
      dataSource: {
        user: utils.parseUser('80xxxxxx', '郭哥哥')
      }
    }
  },
  methods: {
    async submitEvent () {
      let name = ''
      let account = ''
      if (this.dataSource.user && this.dataSource.user.length) {
        account = utils.splitUser(this.dataSource.user)[0]
        name = utils.splitUser(this.dataSource.user)[1]
      }
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify({ name, account })
      })
    }
  }
}
</script>
```

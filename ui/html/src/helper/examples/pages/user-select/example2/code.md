``` html
<template>
  <div>
    <UserSelect
      mode="multiple"
      v-model="dataSource.user"
    />
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
        user: utils.parseUser('80xxxxxx,801xxxxx', '郭哥哥,郭弟弟')
      }
    }
  },
  methods: {
    async submitEvent () {
      let names = ''
      let accounts = ''
      if (this.dataSource.user && this.dataSource.user.length) {
        accounts = utils.splitUser(this.dataSource.user)[0]
        names = utils.splitUser(this.dataSource.user)[1]
      }
      this.$modal.success({
        title: '操作结果',
        content: JSON.stringify({ names, accounts })
      })
    }
  }
}
</script>
```

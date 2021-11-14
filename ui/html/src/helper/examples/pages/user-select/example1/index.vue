<template>
  <Panel :code="code" title="单选人员" :description="description">
    <template slot="example">
      <UserSelect v-model="dataSource.user" />
      <br>
      <br>
      <a-button type="primary" @click="submitEvent">提交</a-button>
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import description from './description.md'
import UserSelect from '@/components/UserSelect'
import utils from '@/utils'
export default {
  title: '单选人员',
  name: 'Example1',
  components: { UserSelect },
  data () {
    return {
      code,
      description,
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

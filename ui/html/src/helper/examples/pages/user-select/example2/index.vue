<template>
  <Panel :code="code" title="多选人员" :description="description">
    <template slot="example">
      <UserSelect
        mode="multiple"
        v-model="dataSource.user"
      />
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
  title: '多选人员',
  name: 'Example2',
  components: { UserSelect },
  data () {
    return {
      code,
      description,
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

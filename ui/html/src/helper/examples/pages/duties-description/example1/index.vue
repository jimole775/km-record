<template>
  <Panel :code="code" title="后端vhtml样例" :description="description">
    <template slot="example">
      <DutiesDescription :modal="modal" />
      <a-button type="primary" @click="modal.show = true">后端vhtml</a-button>
    </template>
  </Panel>
</template>
<script>
import code from './code.md'
import description from './description.md'
import DutiesDescription from '@/components/DutiesDescription'
export default {
  title: '后端vhtml样例',
  name: 'Example1',
  components: {
    DutiesDescription
  },
  data () {
    return {
      code,
      description,
      modal: {
        show: false
      }
    }
  }
}
</script>

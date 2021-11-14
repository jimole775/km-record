``` html
<template>
  <div class="moveBox">
    <DutiesDescription :modal="modal" />
    <a-button type="primary" @click="modal.show = true">后端vhtml</a-button>
  </div>
</template>
<script>
import DutiesDescription from '@/components/DutiesDescription'
export default {
  components: {
    DutiesDescription
  },
  data () {
    return {
      modal: {
        show: false
      }
    }
  }
}
</script>
```

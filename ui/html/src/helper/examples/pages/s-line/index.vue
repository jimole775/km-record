<script>
import { getComponents } from '@/helper/examples/common/util.js'
const { components } = getComponents(require.context('./', true, /(\.vue)$/))
export default {
  functional: true,
  render (h) {
    return (
      <div>
        {
          components.map((comp) => {
            return <comp.component />
          })
        }
      </div>
    )
  }
}
</script>

<script>
import { getComponents } from '@/helper/examples/common/util.js'
const { components } = getComponents(require.context('./', true, /(\.vue)$/))
export default {
  data () {
    return {
      tabProxy: {
        panes: components,
        activeId: components[0].tabId
      }
    }
  },
  render (h) {
    return (
      <div>
        <STabs tab-proxy={this.tabProxy} />
        {
          this.tabProxy.panes.map((pane) => {
            if (this.tabProxy.activeId === pane.tabId) {
              return <pane.component />
            } else {
              return ''
            }
          })
        }
      </div>
    )
  }
}
</script>

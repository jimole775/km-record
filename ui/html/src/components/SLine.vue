<script>
import utils from '@/utils'
export default {
  functional: true,
  name: 'SLine',
  render (h, vm) {
    const { value = '', len = 10, lineEnd = 'ellipsis', rows = 3 } = vm.props || {}
    const style = vm.data.style || {}
    if (!value) return ''
    let sentence = ''
    if (lineEnd === 'break') {
      sentence = utils.breakSentence(value, len, rows)
    }
    if (lineEnd === 'ellipsis') {
      sentence = utils.ellipsisSentence(value, len)
    }
    if (utils.isString(sentence)) {
      if (value === sentence) {
        return <div class="line-standard" style={style}>{ value }</div>
      } else {
        return (
          <a-tooltip title={value}>
            <div class="line-standard" style={style}>{ sentence }</div>
          </a-tooltip>
        )
      }
    } else if (utils.isArray(sentence)) {
      return (
        <a-tooltip title={value}>
          <div class="line-multiple" style={style}>
            {
              sentence.map((line) => {
                return <div>{ line }</div>
              })
            }
          </div>
        </a-tooltip>
      )
    } else {
      return <div class="line-standard" style={style}>{ value }</div>
    }
  }
}
</script>

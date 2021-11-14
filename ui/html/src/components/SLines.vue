<script>
import utils from '@/utils'
export default {
  functional: true,
  name: 'SLines',
  render (h, vm) {
    const { len = 20, value = '', lineEnd = 'ellipsis' } = vm.props || {}
    const style = vm.data.style || {}
    const sentences = getSentences(value)
    return (
      <div style={style}>
        {
          sentences.map((sentence) => {
            if (lineEnd === 'ellipsis') {
              // xxxxx..
              // xxxxx..
              return <SLine style={style} len={len} value={sentence} />
            } else if (lineEnd === 'break') {
              // xxxxxxx
              // xxx
              // xxxxxxx
              // xxxxx
              const lines = utils.breakSentence(sentence, len)
              return lines.map(line => {
                return <div class="line-multiple">{ line }</div>
              })
            } else {
              return ''
            }
          })
        }
      </div>
    )
  }
}

function getSentences (content) {
  // 把所有换行符换成 _||_
  const splitSign = '_||_'
  content = content.replace(/(\r\n)/ig, splitSign)
  content = content.replace(/(\r)/ig, splitSign)
  content = content.replace(/(\n)/ig, splitSign)
  return content.split(splitSign)
}

</script>

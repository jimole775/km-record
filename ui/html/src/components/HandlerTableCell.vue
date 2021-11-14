<script>
export default {
  functional: true,
  name: 'HandlerTableCell',
  render (h, data) {
    const { len = 20, name = '', account = '' } = data.props || {}
    return (
      <SLine len={len} value={spillCurrentHandler(name, account)} />
    )
  }
}
function spillCurrentHandler (nameString, accountString) {
  if (!nameString || !accountString) return ''
  const names = nameString.split(',')
  const accounts = accountString.split(',')
  const res = []
  spackling(names, accounts)
  accounts.forEach((acct, index) => {
    const currentAcct = acct || ''
    const currentName = names[index] || ''
    res.push(`${currentName}(${currentAcct})`)
  })
  return res.join('，')
}
// 填充缺失的数据
function spackling (names, accounts) {
  const diff = names.length - accounts.length
  if (diff > 0) {
    for (let i = 0; i < diff; i++) {
      accounts.push('N/A')
    }
  }
  if (diff < 0) {
    for (let j = diff; j < 0; j++) {
      names.push('N/A')
    }
  }
}

</script>

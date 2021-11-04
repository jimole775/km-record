1. 三键 换 二键
shift p
ctrl p
1 p
1 r
ctrl r
0 p
0 r
shift r

2. 单组合键 
ctrl p
s p
s r
ctrl r

3. 多次组合键
shift p
9 p
9 r
0 p
0 r
shift r

4. 功能键
ctrl p
alt p
i p
i r
alt r
ctrl r

96: 单辅助键
97: 双辅助键
98: 已消费，清除中
99: 触发

status: 99
press { 
  keys: [alt, i]
}
release {
  keys: [alt]
}

record [
  {
    ctrl: { p, t }
  }
  {
    ctrl: { r, t }
  }
  {
    alt: { p, t }
  }
]


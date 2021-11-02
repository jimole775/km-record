# 截去时间戳的前后4位，如果位数不够，用0填充
def skin_time(_t):
  t_str = str(_t)
  s,ss = t_str.split('.')
  ln = len(ss)
  if ln < 7:
    ss = ss + '0' * (7 - ln)
  return s[4:] + '.' + ss[:-4]

# 测试os的移位效果
path = './business/temp/index.log'
file = open(path)
file.seek(1694)
line = file.readline()
while len(line) > 0:
  print(line)
  line = file.readline()

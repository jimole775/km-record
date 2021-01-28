DEFAULT = {
  'match_times': 10, # 对图像中的插入元素，需要等待匹配的次数
  'match_interval': 0.5, # 每次匹配需要等待的时间
  'match_click': True, # 在执行click事件的时候，是否需要匹配有没有目标元素
  'object_name': 'temp', # 录制的项目名，默认为temp
  'assets_path': '.\\business\\' # 录制项目的存储路径
}

import sys
if len(sys.argv) > 1:
  from util.asserts import Assert
  import re
  param_dirty = sys.argv[1]
  param_str = re.search(r'--config:(.+)', param_dirty, re.M|re.I).group(1)
  param_arr = param_str.split(',')
  asserts = Assert()
  for param in param_arr:
    key = param.split('=')[0]
    val = param.split('=')[1]
    if asserts.isNumber(val):
      DEFAULT[key] = val * 1
    if asserts.isBoolean(val):
      DEFAULT[key] = eval(val)
    else:
      DEFAULT[key] = val

class config():
  MATCH_INTERVAL = DEFAULT['match_interval']
  MATCH_CLICK = DEFAULT['match_click']
  MATCH_TIMES = DEFAULT['match_times']
  OBJECT_NAME = DEFAULT['object_name']
  ASSETS_PATH = DEFAULT['assets_path']

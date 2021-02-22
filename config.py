DEFAULT = {
  'match': {
    'times': 10, # 在执行click事件的时候，是否需要匹配有没有目标元素
    'interval': 0.5, # 在执行click事件的时候，是否需要匹配有没有目标元素
  },
  'project': {
    'name': 'temp', # 录制的项目名，默认为temp
    'path': '.\\business\\' # 录制项目的存储路径
  },
  'hotkey': {
    'play': {
      'F1': u'开始',
      'F2': u'循环',
      'F3': u'暂停',
      'F4': u'继续',
      'F5': u'结束',
    },
    'record': {
      'F1': u'开始',
      'F2': u'暂停',
      'F3': u'继续',
      'F4': u'结束',
    }
  }
}

import sys
# 收集命令行参数
if len(sys.argv) > 1:
  from util.spillargv import spillargv
  DEFAULT = spillargv(sys.argv, DEFAULT)

class config():
  MATCH = DEFAULT['match']
  PROJECT = DEFAULT['project']
  HOTKEY = DEFAULT['hotkey']

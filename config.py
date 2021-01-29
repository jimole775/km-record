DEFAULT = {
  'match': {
    'times': 10, # 在执行click事件的时候，是否需要匹配有没有目标元素
    'interval': 0.5, # 在执行click事件的时候，是否需要匹配有没有目标元素
  },
  'object_name': 'temp', # 录制的项目名，默认为temp
  'assets_path': '.\\business\\', # 录制项目的存储路径
  'hotkey_play': {
    'F1': u'开始',
    'F2': u'循环', 
    'F3': u'暂停', 
    'F4': u'继续', 
    'F5': u'结束', 
  },
  'hotkey_record': {
    'F1': u'开始',
    'F2': u'暂停',
    'F3': u'继续',
    'F4': u'结束',
  }
}

import sys
from util.spillargv import spillargv
if len(sys.argv) > 1:
  DEFAULT = spillargv(sys.argv, DEFAULT)

class config():
  MATCH = DEFAULT['match']
  MATCH_INTERVAL = DEFAULT['match']['interval'] if DEFAULT['match'] else 0
  MATCH_TIMES = DEFAULT['match']['times'] if DEFAULT['match'] else 0
  OBJECT_NAME = DEFAULT['object_name']
  ASSETS_PATH = DEFAULT['assets_path']
  HOTKEY_PLAY = DEFAULT['hotkey_play']
  HOTKEY_RECORD = DEFAULT['hotkey_record']

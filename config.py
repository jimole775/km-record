DEFAULT = {
    'match': {
        'times': 10, # 在执行click事件的时候，是否需要匹配有没有目标元素
        'interval': 0.5, # 在执行click事件的时候，是否需要匹配有没有目标元素
    },
    # 'match': False,
    'project': {
        'name': 'temp', # 录制的项目名，默认为temp
        'path': '.\\business\\' # 录制项目的存储路径
    },
    'abbr': { # 缩写字典
        'loc': 'l', # 用于记录坐标的，一般使用数组的形式存储(json转换)
        'key': 'k', # 键盘按键
        'drag': 'd', # 鼠标事件
        'time': 'i', # 时间戳
        'type': 't', # 类型，对应鼠标或者键盘
        'mouse': 'm', # 鼠标
        'move': 'mv', # 鼠标事件-移动
        'press': 'p', # 鼠标事件-按
        'scroll': 's', # 鼠标事件-滚轮
        'release': 'r' # 鼠标事件-放
    },
    'hotkey': {
        'play': {
            'start': {
                'label': u'开始',
                'key': 'ctrl+1'
            },
            'repeat': {
                'label': u'循环',
                'key': 'ctrl+2'
            },
            'pause': {
                'label': u'暂停',
                'key': 'ctrl+3'
            },
            'continue': {
                'label': u'继续',
                'key': 'ctrl+4'
            },
            'stop': {
                'label': u'结束',
                'key': 'ctrl+5'
            }
        },
        'record': {
            'start': {
                'label': u'开始',
                'key': 'ctrl+1'
            },
            'pause': {
                'label': u'暂停',
                'key': 'ctrl+2'
            },
            'continue': {
                'label': u'继续',
                'key': 'ctrl+3'
            },
            'stop': {
                'label': u'结束',
                'key': 'ctrl+4'
            }
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
    ABBR = DEFAULT['abbr']
    PROJECT = DEFAULT['project']
    HOTKEY = DEFAULT['hotkey']
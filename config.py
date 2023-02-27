import os
DEFAULT = {
    # 'match': {
    #     'times': 10, # 在执行click事件的时候，是否需要匹配有没有目标元素
    #     'interval': 0.5, # 在执行click事件的时候，是否需要匹配有没有目标元素
    # },
    'match': False,
    'assets': {
        'path': os.path.abspath('.\\assets\\')
    },
    'project': {
        'name': 'temp', # 录制的项目名，默认为temp
        'path': '.\\business\\' # 录制项目的存储路径
    },
    'abbr': { # 缩写字典
        'loc': 'l', # 用于记录坐标的，一般使用数组的形式存储(json转换)
        'key': 'k', # 键盘按键
        'drag': 'd', # 鼠标拖拽施放事件
        'time': 'i', # 时间戳
        'text': 'tx', # 文本
        'type': 't', # 类型，对应鼠标或者键盘
        'step': 'st', # 记录操作步骤
        'mouse': 'ms', # 鼠标
        'words': 'ws', # 文字
        'move': 'mv', # 鼠标事件-移动
        'press': 'p', # 鼠标事件-按
        'scroll': 's', # 鼠标事件-滚轮
        'release': 'r', # 鼠标事件-放
        'keyboard': 'kb', # 键盘
        'drag_move': 'dm', # 鼠标拖拽过程
        'input_language': 'il', # 当前输入法的语言
        'input_system': 'is', # 当前输入法的系统（微软拼音|搜狗）
        'keyboard_event': 'ke', # 键盘事件类型
        'mouse_event': 'me', # 鼠标事件类型
    },
    'cmd': {
        'random_type': { # 键入随机字符的指令
            'label': u'键入随机数',
            'key': 'ctrl+alt+i'
        }
    },
    'hotkey': {
        'play': {
            'start': {
                'label': u'开始',
                'key': 'ctrl+shift+1'
            },
            'repeat': {
                'label': u'循环',
                'key': 'ctrl+shift+2'
            },
            'pause': {
                'label': u'暂停',
                'key': 'ctrl+shift+3'
            },
            'continue': {
                'label': u'继续',
                'key': 'ctrl+shift+4'
            },
            'stop': {
                'label': u'结束',
                'key': 'ctrl+shift+5'
            }
        },
        'record': {
            'start': {
                'label': u'开始',
                'key': 'ctrl+shift+1'
            },
            'pause': {
                'label': u'暂停',
                'key': 'ctrl+shift+2'
            },
            'continue': {
                'label': u'继续',
                'key': 'ctrl+shift+3'
            },
            'stop': {
                'label': u'结束',
                'key': 'ctrl+shift+4'
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
    ASSETS = DEFAULT['assets']
    CMD = DEFAULT['cmd']


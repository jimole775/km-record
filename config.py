DEFAULT = {
    # 'match': {
    #     'times': 10, # 在执行click事件的时候，是否需要匹配有没有目标元素
    #     'interval': 0.5, # 在执行click事件的时候，是否需要匹配有没有目标元素
    # },
    'match': False,
    'project': {
        'name': 'temp', # 录制的项目名，默认为temp
        'path': '.\\business\\' # 录制项目的存储路径
    },
    'hotkey': {
        'play': {
            'start': {
                'label': u'开始',
                'key': 'F1'
            },
            'repeat': {
                'label': u'循环',
                'key': 'F2'
            },
            'pause': {
                'label': u'暂停',
                'key': 'F3'
            },
            'continue': {
                'label': u'继续',
                'key': 'F4'
            },
            'stop': {
                'label': u'结束',
                'key': 'F5'
            }
        },
        'record': {
            'start': {
                'label': u'开始',
                'key': 'F1'
            },
            'pause': {
                'label': u'暂停',
                'key': 'F2'
            },
            'continue': {
                'label': u'继续',
                'key': 'F3'
            },
            'stop': {
                'label': u'结束',
                'key': 'F4'
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
    PROJECT = DEFAULT['project']
    HOTKEY = DEFAULT['hotkey']
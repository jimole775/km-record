def record (test):
    from config import config
    from core.record import moniting
    from util.mkdir import mkdir
    from util.rmdir import rmdir
    import os
    object_dir = config.PROJECT['path'] + config.PROJECT['name']
    # 如果目录已经存在,先删除之
    if os.path.exists(object_dir) == True:
        rmdir(object_dir)
        mkdir(object_dir)
    else:
        mkdir(object_dir)
    moniting()
    pass


def replay ():
    from core.keyboard import KEvent
    from core.controller import HotKeyCtrl
    kEvent = KEvent(HotKeyCtrl().mount)
    kEvent.start()


def desktop ():
    from core.desktop import Desktop
    desktop = Desktop()
    desktop.registerFunction('record', (record, 1))
    desktop.registerFunction('play', (replay,))
    desktop.open()

# 把第二个指令参数当作函数调用
import sys
if len(sys.argv) > 1:
    argv = sys.argv[1]
    if argv in dir():
        fn_n = eval(argv)
        if callable(fn_n):
            fn_n()
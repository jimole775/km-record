def record ():
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

# 把第二个指令参数当作函数调用
import sys
if len(sys.argv) > 1:
    fn_n = eval(sys.argv[1])
    if callable(fn_n):
        fn_n()
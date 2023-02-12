def record ():
    from core.record import Record
    from core.initbuspace import initbuspace
    initbuspace()
    Record().run()
    pass


def play ():
    from core.play import Play
    Play().run()


def client ():
    from ui.index import open
    open()

# 把第二个指令参数当作函数调用
import sys
if len(sys.argv) > 1:
    argv = sys.argv[1]
    if argv in dir():
        fn_n = eval(argv)
        if callable(fn_n):
            fn_n()
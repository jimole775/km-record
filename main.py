def record ():
    from modules.record import Record
    from modules.initbuspace import initbuspace
    initbuspace()
    Record()
    pass


def play ():
    from modules.play import Play
    Play()


def client ():
    from ui.index import ui_render
    ui_render()

# 把第二个指令参数当作函数调用
import sys
if len(sys.argv) > 1:
    argv = sys.argv[1]
    if argv in dir():
        fn_n = eval(argv)
        if callable(fn_n):
            fn_n()
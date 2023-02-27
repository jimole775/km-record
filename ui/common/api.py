'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:15:30
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:15:40
 # @ Description: 本模块主要用于向 client 主窗口 暴露 python 的方法
 '''

from ui.common.wincompat import px_html_to_py
from ui.common.move_event import MoveEvent
from state.handler import Handler

class Api ():
    def __init__ (self) -> None:
        pass

    def init (self, window):
        self.window = window
        self.state = Handler()
        self.move_event = MoveEvent()
        self.move_event.init(window)
        self.window.events.closed += self.reset
        self.window.events.minimized += self.minimized
        self.window.events.restored += self.restored
        pass

    def move_start (self, x_in_html, y_in_html):
        print('move_start runing')
        self.move_event.mount(x_in_html, y_in_html)
        pass

    def minimized (self):
        pass

    def restored (self):
        # print(self.window.width, self.window.height)
        # w = px_html_to_py(self.window.width)
        # h = px_html_to_py(self.window.height)
        # self.resize(w + 12, h)
        pass

    def resize (self, width, height):
        w = px_html_to_py(width)
        h = px_html_to_py(height)
        self.window.resize(int(w), int(h))
        pass

    def reset (self):
        self.modal = None
        self.window = None
        self.move_event = None
        pass

    def show (self):
        self.window.show()
        pass

    def hide (self):
        self.window.hide()
        pass

    def minimize (self):
        self.window.minimize()
        pass

    def restore (self):
        self.window.restore()
        pass

    def close (self):
        self.window.destroy()
        pass

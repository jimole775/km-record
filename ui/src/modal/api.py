'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:15:30
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:15:40
 # @ Description: 本模块主要用于向 modal 弹窗 暴露 python 的方法
 '''

from ui.util.wincompat import px_html_to_py

class ModalApi ():
    def __init__ (self) -> None:
        pass
    
    def init (self, window):
        self.window = window
        self.window.events.closed += self.reset
        pass

    def move (self, x, y):
        print('move call:', x, y)
        self.window.move(x, y)
        pass

    def resize (self, width, height):
        w = px_html_to_py(width)
        h = px_html_to_py(height)
        self.window.resize(w, h)
        pass

    def show (self):
        self.window.show()
        pass

    def hide (self):
        self.window.hide()
        pass

    def reset (self):
        self.window = None
        pass

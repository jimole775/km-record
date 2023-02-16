'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:15:30
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:15:40
 # @ Description: 本模块主要用于向 client 主窗口 暴露 python 的方法
 '''

from ui.util.wincompat import set_window_size, px_html_to_py, scale_rate
from ui.html.modal import start as modal_start
from ui.util.move_event import MoveEvent

class Api ():
    move_event = MoveEvent()
    def __init__ (self) -> None:
        pass
    
    def set_window (self, window):
        self.move_event.set_window(window)
        self.window = window
        pass
    
    def get_window (self):
        return self.window
    
    # def call (self, fn_name, *params):
    #     print('fn been called:', fn_name, params)
    #     fn_n = eval('self.window.' + fn_name)
    #     fn_n(params)
    #     pass
    
    def move (self, x, y):
        print('move call:', x, y)
        self.window.move(x, y)
        pass

    def move_start (self, x_in_html, y_in_html):
        print('move_start runing')
        self.move_event.mount(x_in_html, y_in_html)
        pass

    def move_end (self):
        print('move_end running')
        self.move_event.unmount()
        pass

    def resize (self, width, height):
        w = px_html_to_py(width)
        h = px_html_to_py(height)
        set_window_size(self.window, w, h)
        pass
    
    def init_modal (self):
        self.modal = modal_start()
        pass
    
    def open_modal (self, modal_name):
        self.modal['ejs'].modal_state(True)
        self.modal['ejs'].modal_route(modal_name)
        self.modal['api'].show()
        pass

    def regist_event ():
        # 只有注册的事件，才能被触发
        pass
    
    def show (self):
        self.window.show()
        pass

    def hide (self):
        self.window.hide()
        pass

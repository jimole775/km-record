'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:15:30
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:15:40
 # @ Description: 本模块主要用于向 modal 弹窗 暴露 python 的方法
 '''

from ui.util.wincompat import set_window_size, wh_html_to_py

class ModalApi ():
    def __init__ (self) -> None:
        pass
    
    def set_window (self, window):
        self.window = window
        pass
    
    def get_window (self):
        return self.window
    
    def call (self, fn_name, *params):
        print('fn been called:', fn_name, params)
        fn_n = eval('self.window.' + fn_name)
        fn_n(params)
        pass
    
    def resize (self, width, height):
        w = wh_html_to_py(w=width)
        h = wh_html_to_py(h=height)
        set_window_size(self.window, w, h)
        pass
    
    def show (self):
        self.window.show()
        pass

    def hide (self):
        self.window.hide()
        pass

'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:31:39
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:31:44
 # @ Description: 本模块主要用于声明和调用client主窗口的js的方法
 '''

from ui.src.client.const import client_size

class EvalJs ():
    def __init__ (self) -> None:
        pass
    
    def set_window (self, window):
        self.window = window
        pass
    
    def get_window (self):
        return self.window
    
    def init (self):
        w = client_size['html_w']
        h = client_size['html_h']
        pass

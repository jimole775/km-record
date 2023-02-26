'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:31:39
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:31:44
 # @ Description: 本模块主要用于声明和调用client主窗口的js的方法
 '''
from ui.common.ejs import EvalJs

class ClientEvalJs (EvalJs):
    def __init__ (self) -> None:
        pass

    def sync_step (self, step):
        self._eval_jsonp(self.sync_step, step)
        pass

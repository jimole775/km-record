'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:31:39
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:31:44
 # @ Description: 本模块主要用于声明和调用 modal弹窗 的 js 的方法
 '''
from ui.util.ejs import EvalJs

class ModalEvalJs (EvalJs):
    def __init__ (self) -> None:
        pass

    def modal_route (self, route_name):
        self._eval_jsonp(self.modal_route, route_name)
        pass

    def modal_state (self, flag):
        self._eval_jsonp(self.modal_state, flag)
        pass

    def update_step (self, step):
        self._eval_jsonp(self.update_step, step)
        pass

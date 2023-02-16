'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:31:39
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:31:44
 # @ Description: 本模块主要用于声明和调用 modal弹窗 的 js 的方法
 '''
import json
from ui.src.modal.const import modal_size

class ModalEvalJs ():
    def __init__ (self) -> None:
        pass
    
    def set_window (self, window):
        self.window = window
        pass

    def get_window (self):
        return self.window
    
    def init (self):
        w = modal_size['html_w']
        h = modal_size['html_h']
        self.default_size(w, h)
        # self.send_data({
        #     "kmr_modal_rect": {
        #         "w": w,
        #         "h": h,
        #         "x": 0,
        #         "y": 0,
        #     }
        # })
        pass

    def _eval_jsonp (self, func, *args):
        js_str = """
            var kmr = window.__kmr__ || {}
            var methodMap = kmr.methods || {}
            var fun = methodMap['%s'] || function () {}
            console.log('global function "%s" being called by webview')
            try {
                fun.apply(null, %s)
            } catch (e) {
                console.error(e.message)
            }
        """%(func.__name__, func.__name__, json.dumps(args))
        self.window.evaluate_js(js_str)

    def send_data (self, data):
        self._eval_jsonp(self.send_data, data)
        pass

    def default_size (self, w, h):
        self._eval_jsonp(self.default_size, w, h)
        pass

    def resize (self, w, h):
        self._eval_jsonp(self.resize, w, h)
        pass

    def move (self, x, y):
        self._eval_jsonp(self.move, x, y)
        pass

    def modal_route (self, route_name):
        self._eval_jsonp(self.move, route_name)
        pass

    def modal_state (self, flag):
        self._eval_jsonp(self.modal_state, flag)
        pass

    def update_step (self, step):
        self._eval_jsonp(self.update_step, step)
        pass

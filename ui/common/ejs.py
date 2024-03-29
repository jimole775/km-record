'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:31:39
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:31:44
 # @ Description: 本模块主要用于声明和调用client主窗口的js的方法
 '''
import json
class EvalJs ():
    def __init__ (self) -> None:
        pass
    
    def init (self, window):
        self.window = window
        pass

    def send_data (self, data):
        self._eval_jsonp(self.send_data, data)
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

    def resize (self, w, h):
        self._eval_jsonp(self.resize, w, h)
        pass

    def default_client_size (self, w, h):
        self._eval_jsonp(self.default_client_size, w, h)
        pass

    def default_modal_size (self, w, h):
        self._eval_jsonp(self.default_modal_size, w, h)
        pass


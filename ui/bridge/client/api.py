'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:15:30
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:15:40
 # @ Description: 本模块主要用于向 client 主窗口 暴露 python 的方法
 '''

from ui.html.modal import start as modal_start
from ui.common.api import Api

class ClientApi (Api):
    def __init__ (self) -> None:
        self.modal = None
        pass

    def init_modal (self):
        # self.modal = modal_start()
        pass

    def open_modal (self, modal_name):
        if not self.modal or not self.modal['api'].window:
            self.modal = modal_start()
        self.modal['ejs'].modal_state(True)
        self.modal['ejs'].modal_route(modal_name)
        self.modal['api'].show()
        pass

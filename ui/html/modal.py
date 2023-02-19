'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:00:34
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:49:13
 # @ Description:
 '''
import webview as mainUI
from ui.src.modal.api import ModalApi
from ui.src.modal.ejs import ModalEvalJs
from ui.src.modal.const import modal_size, ui_style
from flask import Flask, render_template

# 实例化 flask 对象
# 默认 模板目录：templates
# 默认 静态目录：static
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

def start():
    api = ModalApi()
    ejs = ModalEvalJs()
    window = mainUI.create_window('modal',
                                    url='http://localhost:9999/modal',    
                                    js_api=api,width=modal_size['init_w'], height=modal_size['init_h'],
                                    x=None, y=None, resizable=False, fullscreen=False,
                                    hidden=False, frameless=True, easy_drag=True,
                                    minimized=False, on_top=True, confirm_close=False,
                                    transparent=False, text_select=False, background_color=ui_style['primary_background_color'])
    api.init(window)
    ejs.init(window)
    w = modal_size['html_w']
    h = modal_size['html_h']
    ejs.default_html_size(w, h)
    return { 'api': api, 'ejs': ejs }

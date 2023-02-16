'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:00:34
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:49:13
 # @ Description:
 '''
import webview as mainUI
from ui.src.client.api import Api
from ui.src.client.ejs import EvalJs
from ui.src.client.const import client_size, ui_style
from flask import Flask, render_template

# 实例化 flask 对象
# 默认 模板目录：templates
# 默认 静态目录：static
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

def start():
    api = Api()
    ejs = EvalJs()
    window = mainUI.create_window('main',
                                    url='http://localhost:9999/',    
                                    js_api=api,width=client_size['init_w'], height=client_size['init_h'],
                                    x=None, y=None, resizable=False, fullscreen=False,
                                    hidden=False, frameless=True, easy_drag=True,
                                    minimized=False, on_top=True, confirm_close=True,
                                    transparent=True, text_select=False, background_color=ui_style['primary_background_color'])
    api.set_window(window)
    ejs.set_window(window)
    mainUI.start(func=ejs.init, gui='cef', debug=True)

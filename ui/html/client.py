'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:00:34
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:49:13
 # @ Description:
 '''
import webview as mainUI
from ui.src.client.api import ClientApi
from ui.src.client.ejs import ClientEvalJs
from ui.src.client.const import client_size, ui_style
from flask import Flask, render_template

# 实例化 flask 对象
# 默认 模板目录：templates
# 默认 静态目录：static
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

def init (api, ejs, win):
    api.init(win)
    ejs.init(win)
    ejs.default_client_size(client_size['html_w'], client_size['html_h'])
    pass

def start():
    api = ClientApi()
    ejs = ClientEvalJs()
    window = mainUI.create_window('main',
                                    url='http://localhost:9999/',    
                                    js_api=api,width=client_size['init_w'], height=client_size['init_h'],
                                    x=None, y=None, resizable=False, fullscreen=False,
                                    hidden=False, frameless=True, easy_drag=True,
                                    minimized=False, on_top=True, confirm_close=True,
                                    transparent=False, text_select=False, background_color=ui_style['primary_background_color'])

    mainUI.start(func=init, args=[api, ejs, window], gui='edgechromium', debug=True)

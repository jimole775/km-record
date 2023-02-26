'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:25:44
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:25:49
 # @ Description: 主窗口的常量声明
 '''

from ui.common.wincompat import px_py_to_html, wh_tolerance

_base_rect = {
    'w': 1000,
    'h': 350,
    'x': 0,
    'y': 0,
}

"""
在 win10 中，如果用户设置了【字体缩放】，
那么，webview 在 create_window 时，参数中的 width 和 height 所呈现的效果
和 window.resize() 是不一致的，所以，这里需要特别定制一个 init_w, init_h
当然，这只是一台机器的情况，如果其他机器有问题，再另做打算
"""
client_size = {
    'py_w': _base_rect['w'],
    'py_h': _base_rect['h'],
    'html_w': int(px_py_to_html(_base_rect['w'])),
    'html_h': int(px_py_to_html(_base_rect['h'])),
    'init_w': int(_base_rect['w'] + wh_tolerance['w']),
    'init_h': int(_base_rect['h'] + wh_tolerance['h']),
}

ui_style = {
    'primary_font_color': '#D1D1D2',
    'primary_background_color': '#1C1C1F'
}

'''
 # @ Author: Your name
 # @ Create Time: 2023-02-12 22:01:47
 # @ Modified by: Your name
 # @ Modified time: 2023-02-12 22:01:50
 # @ Description:
 '''

from win32 import win32gui, win32print
from win32.lib import win32con

from win32.win32api import GetSystemMetrics

wh_tolerance = {
    'w': 16,
    'h': 48,
}

scale_rate = round(win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES) / GetSystemMetrics(0), 2)

def set_window_size (win, w, h):
    """
    根据 https://github.com/r0x0r/pywebview/issues/589 的反馈，
    在 pywebview 3.x 版本的 CEF 渲染器中 webview.platforms.cef.Browser 中的 resize 方法中
    `webview.platforms.cef.windll.user32.SetWindowPos(self.inner_hwnd, 0, 0, 0, width - 16, height - 38,...`
    这一段，会导致设置高宽时，出现空白间隙，我们需要在调用时重新补全
    :::这两个数值的间隙，是底层代码留给 titlebar 和 scrollbar 的
    """
    win.resize(w + wh_tolerance['w'], h + wh_tolerance['h'])
    pass

def px_html_to_py (val):
    return val * scale_rate

def px_py_to_html (val):
    return val / scale_rate

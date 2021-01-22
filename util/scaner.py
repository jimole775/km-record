import win32gui
from PIL import Image, ImageGrab
class FindWindow:
  def __init__(self, wdname):
    """初始化"""
    # 取得窗口句柄
    self.hwnd = win32gui.FindWindow(0, wdname)
    if not self.hwnd:
      print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
      exit()
    # 窗口显示最前面
    win32gui.SetForegroundWindow(self.hwnd)
  def position(self):
    return win32gui.GetWindowRect(self.hwnd)
  # def cutScreen(self):
  #   x1, y1, x2, y2 = win32gui.GetWindowRect(self.hwnd)
  #   print(x1, y1, x2, y2)
  #   return ImageGrab.grab((x1, y1, x2, y2))

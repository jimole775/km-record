import pyautogui as gui
import numpy as np
class Replay():
  def start(self, index, x, y):
    """初始化"""
    # loc=np.where(coord<0.1)
    # loc = cv.minMaxLoc(coord)
    print('loc:', x, y)
    # sleep(1000)
    gui.moveTo(x, y)
    gui.click()
    if (index == 8):
      gui.moveTo(x + 120, y + 20)
      gui.click()
      gui.typewrite('sss')
    if (index == 9):
      gui.typewrite('123')
    # # 取得窗口句柄
    # self.hwnd = win32gui.FindWindow(0, wdname)
    # if not self.hwnd:
    #   print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
    #   exit()
    # # 窗口显示最前面
    # win32gui.SetForegroundWindow(self.hwnd)
  # def cutScreen(self):
  #   x1, y1, x2, y2 = win32gui.GetWindowRect(self.hwnd)
  #   print(x1, y1, x2, y2)
  #   return ImageGrab.grab((x1, y1, x2, y2))

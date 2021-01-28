import win32gui
import time
import cv2 as cv
import numpy as np
from PIL import Image, ImageGrab
class Scaner:
  def __init__(self):
    x,y = ImageGrab.grab().size
    self.win = (0, 0, x, y)
    self.bbox = (0, 0, 0, 0)
  def findWindow(self, wdname):
    """初始化"""
    # 取得窗口句柄
    self.hwnd = win32gui.FindWindow(0, wdname)
    if not self.hwnd:
      print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
      exit()
    # 窗口显示最前面
    win32gui.SetForegroundWindow(self.hwnd)
    self.bbox = win32gui.GetWindowRect(self.hwnd)
    return ImageGrab.grab(self.bbox)

  """
  # 匹配唯一坐标，结果可能有3种：
  # 1. 唯一匹配
  # 2. 不唯一匹配
  # 3. 无匹配
  """
  def hasUniqueTarget(self, screen, temp):
    if type(screen) == str:
      screen = cv.imread(screen, 0)
    if type(temp) == str:
      temp = cv.imread(temp, 0)
    cv_temp = cv.cvtColor(np.array(temp), cv.COLOR_RGB2BGR)
    cv_bg = cv.cvtColor(np.array(screen), cv.COLOR_RGB2BGR)
    res = cv.matchTemplate(cv_bg, cv_temp, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold) # 返回下标
    print('hasUniqueTarget:', len(loc), len(loc[0]), len(loc[1]))
    if len(loc) > 0 and len(loc[0]) == 1:
      return True
    else:
      return False

  def locate(self, origin, tempPath):
    # temp = Image.open(tempPath)
    # temp = 255 * np.array(temp).astype('uint8')
    # temp = cv.cvtColor(np.array(temp), cv.COLOR_RGB2BGR)  # PIL转cv
    # 选择匹配算法
    cv_origin = cv.cvtColor(np.array(origin), cv.COLOR_RGB2BGR)  # PIL转cv
    cv_temp = cv.cvtColor(np.array(cv.imread(tempPath, 0)), cv.COLOR_RGB2BGR) # PIL转cv

    gray_origin = cv.cvtColor(cv_origin, cv.COLOR_BGR2GRAY)
    gray_temp = cv.cvtColor(cv_temp, cv.COLOR_BGR2GRAY)
    # cv.imwrite('res_bg.jpg', bg)
    # cv.imwrite('res_temp.jpg', temp)
    match_method = cv.TM_CCOEFF_NORMED
    # cv2.TM_CCOEFF_NORMED
    res = cv.matchTemplate(gray_origin, gray_temp, match_method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # print(min_val, max_val, min_loc, max_loc)
    return (min_loc, max_loc)
  # def cutScreen(self):
  #   x1, y1, x2, y2 = win32gui.GetWindowRect(self.hwnd)
  #   print(x1, y1, x2, y2)
  #   return ImageGrab.grab((x1, y1, x2, y2))

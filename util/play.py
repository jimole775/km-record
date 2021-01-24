import pyautogui as gui
import numpy as np
import cv2 as cv
import os
import re
import time
from config import config
from util.scissors import Scissors
class Play:
  def __init__(self):
    self.play_type = 'single'
    self.pause_sign = False
    self.stop_sign = False
    self.step = 0
    self.step_at_pause = 0
    self.step_items = []
    self.scissors = Scissors()
    self.check_times = 10 # 检查次数，暂时弃用，避免漏帧
    self.interval_sec = 0.5 # 检查的间隔时间
    pass

  def getSteps(self, objectDir):
    i = 0
    file_list = os.listdir(objectDir)
    for file_name in file_list:
      timestamp = re.search(r'^\d*?\.?\d*?(?=\_)', file_name).group()
      loc = eval(re.search(r'\(\d*?, \d*?\)', file_name).group())
      insert = re.search(r'insert', file_name).group()
      nextTime = self.getNextTime(i, file_list)
      self.step_items.append({
        'loc': loc,
        'insert': insert,
        'file': objectDir + '\\' + file_name,
        'sleep': float(nextTime) - float(timestamp),
      })
      i = i + 1
    pass

  def getNextTime(self, cur_index, file_list):
    if cur_index < len(file_list) - 1:
      nextFile = file_list[cur_index + 1]
    else:
      nextFile = file_list[cur_index]
    return re.search(r'^\d*?\.?\d*?(?=\_)', nextFile).group()

  def doplay(self):
    if self.play_type == 'single':
      self.single()
    if self.play_type == 'repeat':
      self.repeat()

  # def initRunVar(self):
  #   waiting_sec = 0 # 匹配目标图像时等待的时间，持续叠加
  #   return (check_times, waiting_sec, interval_sec)

  def runHandler(self):
    while self.step < len(self.step_items):
      if (self.pause_sign or self.stop_sign):
        break
      cur_step_item = self.step_items[self.step]
      if config.MATCH_CLICK:
        if self.hasCorrectImg(cur_step_item) or self.check_times == 0:
          self.resetCheckTimes()
          self.doclick(cur_step_item)
          self.waiting(cur_step_item['sleep'] - self.check_times * self.interval_sec)
          self.stepGrow()
        else:
          self.checkReduce()
          self.waiting(self.interval_sec)
      else:
        self.doclick(cur_step_item)
        self.waiting(self.interval_sec)
        self.stepGrow()


  def doclick(self, cur_step_item):
    x, y = cur_step_item['loc']
    gui.moveTo(x, y)
    """
    # 移动到目标位置之后，需要等待一个时间间隔单位
    # 以防止有些操作，鼠标移上去还需要网络响应，
    # 点击过快会导致操作丢失
    """
    time.sleep(self.interval_sec)
    gui.click()

  def waiting(self, t_remian):
    if t_remian > self.interval_sec:
      time.sleep(t_remian)
    else:
      time.sleep(self.interval_sec)

  def checkReduce(self):
    self.check_times = self.check_times - 1

  def resetCheckTimes(self):
    self.check_times = 10

  def stepGrow(self):
    self.step = self.step + 1

  def start(self, type = 'single'):
    self.play_type = type
    self.stop_sign = False
    self.pause_sign = False
    self.step = 0
    self.doplay()

  def stop(self):
    self.stop_sign = True
    print('stop play')
    pass

  def _pause(self):
    self.pause_sign = True
    self.step_at_pause = self.step
    print('pause:', self.step)
    pass

  def _continue(self):
    self.stop_sign = False
    self.pause_sign = False
    self.step = self.step_at_pause
    print('continue:', self.step)
    self.doplay()
    pass

  # def stepGrow(self):
  #   print('flow step:', self.step)
  #   if (self.pause_sign or self.stop_sign):
  #     return len(self.step_items)
  #   else:
  #     return self.step + 1

  def single(self):
    self.play_type = 'single'
    self.runHandler()

  def repeat(self):
    self.play_type = 'repeat'
    while self.pause_sign == False and self.stop_sign == False:
      self.runHandler()
      self.step = 0

  def hasCorrectImg(self, cur_step_item):
    x, y = cur_step_item['loc']
    file = cur_step_item['file']
    loc = (x - 50, y - 50, x + 50, y + 50)
    template = cv.imread(file, 0)
    cv_temp = cv.cvtColor(np.array(template), cv.COLOR_RGB2BGR) # PIL转cv
    res = cv.matchTemplate(self.scissors.cutScreen(loc).img, cv_temp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    if (max_loc[0] > 0 and max_loc[1] > 0):
      return True
    else:
      return False



# if (index == 8):
#   gui.moveTo(x + 120, y + 20)
#   gui.click()
#   gui.typewrite('sss')
# if (index == 9):
#   gui.typewrite('123')

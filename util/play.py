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
    self.check_times = config.MATCH_TIMES # 检查次数
    pass

  def getSteps(self, objectDir):
    i = 0
    file_list = os.listdir(objectDir)
    for file_name in file_list:
      timestamp = re.search(r'^\d*?\.?\d*?(?=\_)', file_name).group()
      loc = eval(re.search(r'\(\d*?, \d*?\)', file_name).group())
      insert = re.search(r'insert', file_name)
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

  def runHandler(self):
    while self.step < len(self.step_items):
      if (self.pause_sign or self.stop_sign):
        break
      cur_step_item = self.step_items[self.step]
      """
      # 录制时截取的图片, 是鼠标移动到目标位置，点击之后的,
      # 那么, 需要准确的记录出移动到目的地之后的滞留时间
      """
      self.domove(cur_step_item)
      if config.MATCH_CLICK:
        if self.hasCorrectImg(cur_step_item) or self.check_times == 0:
          self.resetCheckTimes()
          self.doclick(cur_step_item)
          self.stepGrow()
          self.waiting(cur_step_item['sleep'] - self.checkedSeconds())
        else:
          self.checkReduce()
          self.waiting(config.MATCH_INTERVAL)
      else:
        self.doclick(cur_step_item)
        self.stepGrow()
        self.waiting(config.MATCH_INTERVAL)

  def checkedSeconds(self):
    return (config.MATCH_TIMES - self.check_times) * config.MATCH_INTERVAL

  def domove(self, cur_step_item):
    x, y = cur_step_item['loc']
    gui.moveTo(x, y)
    time.sleep(config.MATCH_INTERVAL)

  def doclick(self, cur_step_item):
    x, y = cur_step_item['loc']
    gui.moveTo(x, y)
    gui.click()

  def waiting(self, t_remian):
    if t_remian > config.MATCH_INTERVAL:
      time.sleep(t_remian)
    else:
      time.sleep(config.MATCH_INTERVAL)

  def checkReduce(self):
    print('check_times:', self.check_times)
    self.check_times = self.check_times - 1

  def resetCheckTimes(self):
    self.check_times = config.MATCH_TIMES

  def stepGrow(self):
    self.step = self.step + 1
    print('step:', self.step)

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

  def single(self):
    self.play_type = 'single'
    self.runHandler()

  def repeat(self):
    self.play_type = 'repeat'
    while self.pause_sign == False and self.stop_sign == False:
      self.runHandler()
      self.step = 0

  def hasCorrectImg(self, cur_step_item):
    file = cur_step_item['file']
    template = cv.imread(file, 0)
    cv_temp = cv.cvtColor(np.array(template), cv.COLOR_RGB2BGR) # PIL转cv
    cv_bg = self.scissors.cutScreen().img
    res = cv.matchTemplate(cv_bg, cv_temp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    if (max_loc[0] > 0 and max_loc[1] > 0):
      self.fixLocator(cur_step_item, max_loc)
      return True
    else:
      return False

  def fixLocator(self, cur_step_item, max_loc):
    cur_step_item['loc'] = max_loc

# if (index == 8):
#   gui.moveTo(x + 120, y + 20)
#   gui.click()
#   gui.typewrite('sss')
# if (index == 9):
#   gui.typewrite('123')

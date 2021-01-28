import pyautogui as gui
import numpy as np
import cv2 as cv
import os
import re
import time
from config import config
from util.scaner import Scaner
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
    self.scaner = Scaner()
    self.check_times = config.MATCH_TIMES # 检查次数
    pass

  def _getNextTime(self, cur_index, file_list):
    if cur_index < len(file_list) - 1:
      nextFile = file_list[cur_index + 1]
    else:
      nextFile = file_list[cur_index]
    return re.search(r'^\d*?\.?\d*?(?=\_)', nextFile).group()

  def _runHandler(self):
    while self.step < len(self.step_items):
      if (self.pause_sign or self.stop_sign):
        break
      step_item = self.step_items[self.step]
      """
      # 录制时截取的图片, 是鼠标移动到目标位置，点击之后的,
      # 那么, 需要准确的记录出移动到目的地之后的滞留时间
      """
      self._domoves(step_item)
      if config.MATCH_CLICK:
        if self.scaner.hasUniqueTarget(step_item['file']) or self.check_times == 0:
          self._resetCheckTimes()
          self._doclick(step_item)
          self._stepGrow()
          self._waiting(step_item['sleep'] - self._checkedSeconds())
        else:
          self._checkReduce()
          self._waiting(config.MATCH_INTERVAL)
      else:
        self._doclick(step_item)
        self._stepGrow()
        self._waiting(config.MATCH_INTERVAL)

  # 计算匹配消耗的时间
  def _checkedSeconds(self):
    return (config.MATCH_TIMES - self.check_times) * config.MATCH_INTERVAL

  def _domoves(self, step_item):
    x, y = step_item['loc']
    gui.moveTo(x, y)
    time.sleep(config.MATCH_INTERVAL)

  def _doclick(self, step_item):
    x, y = step_item['loc']
    gui.moveTo(x, y)
    gui.click()

  def _waiting(self, t_remian):
    if t_remian > config.MATCH_INTERVAL:
      time.sleep(t_remian)
    else:
      time.sleep(config.MATCH_INTERVAL)

  def _checkReduce(self):
    print('check_times:', self.check_times)
    self.check_times = self.check_times - 1

  def _resetCheckTimes(self):
    self.check_times = config.MATCH_TIMES

  def _stepGrow(self):
    self.step = self.step + 1
    print('step:', self.step)

  def _doplay(self):
    if self.play_type == 'single':
      self.single()
    if self.play_type == 'repeat':
      self.repeat()

  def start(self, type = 'single'):
    self.play_type = type
    self.stop_sign = False
    self.pause_sign = False
    self.step = 0
    self._doplay()

  def stop(self):
    self.stop_sign = True
    print('stop play')
    pass

  def pause(self):
    self.pause_sign = True
    self.step_at_pause = self.step
    print('pause:', self.step)
    pass

  def continues(self):
    self.stop_sign = False
    self.pause_sign = False
    self.step = self.step_at_pause
    print('continue:', self.step)
    self._doplay()
    pass

  def single(self):
    self.play_type = 'single'
    self._runHandler()

  def repeat(self):
    self.play_type = 'repeat'
    while self.pause_sign == False and self.stop_sign == False:
      self._runHandler()
      self.step = 0

  def getSteps(self, objectDir):
    i = 0
    file_list = os.listdir(objectDir)
    for file_name in file_list:
      timestamp = re.search(r'^\d*?\.?\d*?(?=\_)', file_name).group()
      loc = eval(re.search(r'\(\d*?, \d*?\)', file_name).group())
      insert = re.search(r'insert', file_name)
      nextTime = self._getNextTime(i, file_list)
      self.step_items.append({
        'loc': loc,
        'insert': insert,
        'file': objectDir + '\\' + file_name,
        'sleep': float(nextTime) - float(timestamp),
      })
      i = i + 1
    pass

  # def hasCorrectImg(self, step_item):
  #   file = step_item['file']
  #   template = cv.imread(file, 0)
  #   cv_temp = cv.cvtColor(np.array(template), cv.COLOR_RGB2BGR) # PIL转cv
  #   cv_bg = self.scissors.cutScreen()
  #   res = cv.matchTemplate(cv_bg, cv_temp, cv.TM_CCOEFF_NORMED)
  #   min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
  #   if (max_loc[0] > 0 and max_loc[1] > 0):
  #     self.fixLocator(step_item, max_loc)
  #     return True
  #   else:
  #     return False

  # def fixLocator(self, step_item, max_loc):
  #   step_item['loc'] = max_loc

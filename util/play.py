import pyautogui as gui
import numpy as np
import cv2 as cv
import os
import re
import time
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
    pass

  def getSteps(self, objectDir):
    i = 0
    file_list = os.listdir(objectDir)
    for file_name in file_list:
      timestamp = re.search(r'^\d*?\.?\d*?(?=\_)', file_name).group()
      loc = eval(re.search(r'\(\d*?, \d*?\)', file_name).group())
      nextTime = self.getNextTime(i, file_list)
      self.step_items.append({
        'loc': loc,
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

  def start(self, type = 'single'):
    self.play_type = type
    self.stop_sign = False
    self.pause_sign = False
    self.step = 0
    self.doplay()

  def doplay(self):
    if self.play_type == 'single':
      self.single()
    if self.play_type == 'repeat':
      self.repeat()

  def runHandler(self):
    while self.step < len(self.step_items):
      print('flow step:', self.step)
      cur_step_item = self.step_items[self.step]
      x, y = cur_step_item['loc']
      if self.hasCorrectImg(cur_step_item['file']):
        gui.moveTo(x, y)
        gui.click()
        time.sleep(cur_step_item['sleep'])
        self.step = self.stepGrowp()
      else:
        time.sleep(0.5)

  def stop(self):
    self.stop_sign = True
    self.step = len(self.step_items)
    pass

  def _pause(self):
    self.pause_sign = True
    self.step_at_pause = self.step
    self.step = len(self.step_items)
    print('_pause step:', self.step)
    pass

  def _continue(self):
    self.pause_sign = False
    self.step = self.step_at_pause
    print('continue step:', self.step)
    self.doplay()
    pass

  def stepGrowp(self):
    if (self.pause_sign or self.stop_sign):
      return len(self.step_items)
    else:
      return self.step + 1

  def single(self):
    self.play_type = 'single'
    self.runHandler()

  def repeat(self):
    self.play_type = 'repeat'
    while self.pause_sign == False and self.stop_sign == False:
      self.runHandler()
      self.step = 0

  def hasCorrectImg(self, file):
    template = cv.imread(file, 0)
    cv_temp = cv.cvtColor(np.array(template), cv.COLOR_RGB2BGR) # PIL转cv
    res = cv.matchTemplate(self.scissors.cutScreen().img, cv_temp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # print(max_loc[0], max_loc[1])
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

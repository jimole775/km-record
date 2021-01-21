import pyautogui as gui
import numpy as np
import os
import re
import time
class Play:
  def __init__(self):
    self.play_type = 'single'
    self.pause_sign = False
    self.stop_sign = False
    self.step = 0
    self.step_at_pause = 0
    self.step_items = [
      # {
      #   'loc': (0,0),
      #   'file': path + name,
      #   'sleep': 0
      # }
    ]
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
      gui.moveTo(x, y)
      gui.click()
      time.sleep(cur_step_item['sleep'])
      self.step = self.stepGrowp()

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
    self.runHandler()

  def repeat(self):
    while self.pause_sign == False and self.stop_sign == False:
      self.runHandler()
      self.step = 0

# if (index == 8):
#   gui.moveTo(x + 120, y + 20)
#   gui.click()
#   gui.typewrite('sss')
# if (index == 9):
#   gui.typewrite('123')

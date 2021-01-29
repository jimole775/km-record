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

  def __getNextTime__(self, cur_index, file_list):
    if cur_index < len(file_list) - 1:
      nextFile = file_list[cur_index + 1]
    else:
      nextFile = file_list[cur_index]
    return re.search(r'^\d*?\.?\d*?(?=\_)', nextFile).group()

  def __runHandler__(self):
    while self.step < len(self.step_items):
      if (self.pause_sign or self.stop_sign):
        break
      step_item = self.step_items[self.step]
      """
      # 录制时截取的图片, 是鼠标移动到目标位置，点击之后的,
      # 那么, 需要准确的记录出移动到目的地之后的滞留时间
      """
      self.__domoves__(step_item)
      if config.MATCH_CLICK:
        screen = ImageGrab.grab()
        temp = step_item['file']
        if self.scaner.hasUniqueTarget(screen, temp) or self.check_times == 0:
          self.__resetCheckTimes__()
          self.__doclick__(step_item)
          self.__stepGrow__()
          self.__waiting__(step_item['sleep'] - self.__checkedSeconds__())
        else:
          self.__checkReduce__()
          self.__waiting__(config.MATCH_INTERVAL)
      else:
        self.__doclick__(step_item)
        self.__stepGrow__()
        self.__waiting__(config.MATCH_INTERVAL)

  # 计算匹配消耗的时间
  def __checkedSeconds__(self):
    return (config.MATCH_TIMES - self.check_times) * config.MATCH_INTERVAL

  def __domoves__(self, step_item):
    x, y = step_item['loc']
    gui.moveTo(x, y)
    time.sleep(config.MATCH_INTERVAL)

  def __doclick__(self, step_item):
    x, y = step_item['loc']
    gui.moveTo(x, y)
    gui.click()

  def __waiting__(self, t_remian):
    if t_remian > config.MATCH_INTERVAL:
      time.sleep(t_remian)
    else:
      time.sleep(config.MATCH_INTERVAL)

  def __checkReduce__(self):
    print('check_times:', self.check_times)
    self.check_times = self.check_times - 1

  def __resetCheckTimes__(self):
    self.check_times = config.MATCH_TIMES

  def __stepGrow__(self):
    self.step = self.step + 1
    print('step:', self.step)

  def __doplay__(self):
    if self.play_type == 'single':
      self.single()
    if self.play_type == 'repeat':
      self.repeat()

  def start(self, type = 'single'):
    self.play_type = type
    self.stop_sign = False
    self.pause_sign = False
    self.step = 0
    self.__doplay__()

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
    self.__doplay__()
    pass

  def single(self):
    self.play_type = 'single'
    self.__runHandler__()

  def repeat(self):
    self.play_type = 'repeat'
    while self.pause_sign == False and self.stop_sign == False:
      self.__runHandler__()
      self.step = 0

  def getSteps(self, objectDir):
    i = 0
    file_list = os.listdir(objectDir)
    for file_name in file_list:
      timestamp = re.search(r'^\d*?\.?\d*?(?=\_)', file_name).group()
      loc = eval(re.search(r'\(\d*?, \d*?\)', file_name).group())
      insert = re.search(r'insert', file_name)
      nextTime = self.__getNextTime__(i, file_list)
      self.step_items.append({
        'loc': loc,
        'insert': insert,
        'file': objectDir + '\\' + file_name,
        'sleep': float(nextTime) - float(timestamp),
      })
      i = i + 1
    pass

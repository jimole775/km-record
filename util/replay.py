from config import config
import pyautogui as gui
import numpy as np
import os
import re
import time
class Replay:
  def __init__(self):
    self.objectDir = config.ASSETS_PATH + config.OBJECT_NAME
    self.steps = [
      # {
      #   'loc': (0,0),
      #   'file': path + name,
      #   'sleep': 0
      # }
    ]
    pass
  def getSteps(self):
    loop = 0
    fileList = os.listdir(self.objectDir)
    for fileName in fileList:
      timestamp = re.search(r'^\d*?\.?\d*?(?=\_)', fileName).group()
      loc = eval(re.search(r'\(\d*?, \d*?\)', fileName).group())
      nextTime = self.getNextTime(loop, fileList)
      self.steps.append({
        'loc': loc,
        'file': self.objectDir + '\\' + fileName,
        'sleep': float(nextTime) - float(timestamp),
      })
      loop = loop + 1
    pass
  def run(self):
    loop = 0
    while loop < len(self.steps):
      curStep = self.steps[loop]
      x, y = curStep['loc']
      gui.moveTo(x, y)
      gui.click()
      time.sleep(curStep['sleep'])
      loop = loop + 1
  def getNextTime(curIndex, fileList):
    if curIndex < len(fileList) - 1:
      nextFile = fileList[curIndex + 1]
    else:
      nextFile = fileList[curIndex]
    return re.search(r'^\d*?\.?\d*?(?=\_)', nextFile).group()
# if (index == 8):
#   gui.moveTo(x + 120, y + 20)
#   gui.click()
#   gui.typewrite('sss')
# if (index == 9):
#   gui.typewrite('123')

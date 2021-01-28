from PIL import Image, ImageGrab
from config import config
from util.scaner import Scaner
import cv2 as cv
import numpy as np
import time
import threading
class Scissors:
  def __init__(self):
    self.point = ''
    self.loopTimes = 1
    self.rectLoc = ''
    self.timestamp = ''
    self.img = ''
    self.saveDir = config.ASSETS_PATH + config.OBJECT_NAME
    self.scaner = Scaner()

  def cutUniqueReact(self, point):
    thread = threading.Thread(target=self._cutUniqueReact, args=(point,))
    thread.start()

  def _cutUniqueReact(self, point):
    react = self.cutReact(point)
    if not self.scaner.hasUniqueTarget(react):
      time.sleep(0.5)
      self.loopGrow()
      return self.cutUniqueReact(point)
    else:
      self.loopReset()
      self.save(react)

  def loopGrow(self):
    self.loopTimes = self.loopTimes + 1

  def loopReset(self):
    self.loopTimes = 1

  def cutReact(self, point):
    x, y = point
    self.point = point
    self.rectLoc = self.countReactLoc(x, y)
    self.timestamp = time.time()
    self.img = cv.cvtColor(np.array(ImageGrab.grab(self.rectLoc)), cv.COLOR_RGB2BGR)
    return self.img

  def countReactLoc(self, x, y):
    return (x - self.loopTimes * 50, y - self.loopTimes * 50, x + self.loopTimes * 50, y + self.loopTimes * 50)

  def cutScreen(self):
    self.timestamp = time.time()
    self.img = cv.cvtColor(np.array(ImageGrab.grab()), cv.COLOR_RGB2BGR)
    return self.img

  def save(self, img):
    fileName = str(self.timestamp) + '_' + str(self.point) + '.jpg'
    cv.imwrite(self.saveDir + '\\' + fileName, img)
    return self

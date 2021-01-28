from PIL import Image, ImageGrab
from config import config
from util.scaner import Scaner
import cv2 as cv
import numpy as np
import time
import threading
class Scissors:
  def __init__(self):
    self.timestamp = None
    self.saveDir = config.ASSETS_PATH + config.OBJECT_NAME
    self.scaner = Scaner()

  def _uniqueHandle(self, screen, point, i):
    temp = self.cutReact(screen, point, i)
    if self.scaner.hasUniqueTarget(screen, temp):
      self.save(point, temp)
    else:
      time.sleep(0.5)
      i = i + 1
      return self._uniqueHandle(screen, point, i)

  def _countReactSize(self, point, zoom):
    x, y = point
    return (x - zoom * 50, y - zoom * 50, x + zoom * 50, y + zoom * 50)

  def cutUniqueReact(self, screen, point):
    thread = threading.Thread(target=self._uniqueHandle, args=(screen, point, 1,))
    thread.start()

  def cutReact(self, screen, point, zoom=1):
    print('zoom:', point, zoom)
    x1,y1,x2,y2 = self._countReactSize(point, zoom)
    self.timestamp = time.time()
    cv_screen = self._toCVImg(screen)
    return cv_screen[x1:x2, y1:y2]

  def cutReactAndSave(self, screen, point):
    temp = self.cutReact(screen, point)
    return self.save(point, temp)

  def cutScreen(self):
    self.timestamp = time.time()
    return ImageGrab.grab()

  def save(self, point, temp):
    cv_temp = self._toCVImg(temp)
    fileName = str(self.timestamp) + '_' + str(point) + '.jpg'
    cv.imwrite(self.saveDir + '\\' + fileName, cv_temp)
    return self

  def _toCVImg(self, img):
    return cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)



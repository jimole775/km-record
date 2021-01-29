from PIL import Image, ImageGrab
from config import config
from util.scaner import Scaner
import cv2 as cv
import numpy as np
import time
import threading
class Scissors:
  def __init__(self):
    self.saveDir = config.ASSETS_PATH + config.OBJECT_NAME
    self.scaner = Scaner()

  def cutUniqueReact(self, screen, point):
    cv_screen = self.__pl2cv__(screen)
    thread = threading.Thread(target=self.__uniqueHandle__, args=(cv_screen, point, 1,))
    thread.start()

  def cutReact(self, screen, point, zoom=1):
    x1,y1,x2,y2 = self.__countReactSize__(screen, point, zoom)
    cv_screen = self.__pl2cv__(screen)
    return cv_screen[y1:y2, x1:x2]

  def cutReactAndSave(self, screen, point):
    temp = self.cutReact(screen, point)
    return self.save(point, temp)

  def cutScreen(self):
    return ImageGrab.grab()

  def save(self, point, temp):
    cv_temp = self.__pl2cv__(temp)
    fileName = str(time.time()) + '_' + str(point) + '.jpg'
    cv.imwrite(self.saveDir + '\\' + fileName, cv_temp)
    return self

  def __pl2cv__(self, img):
    if (isinstance(img, Image.Image)):
      return cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    else:
      return img

  def __uniqueHandle__(self, sv_screen, point, i):
    temp = self.cutReact(sv_screen, point, i)
    if self.scaner.hasUniqueTarget(sv_screen, temp) or i == 10:
      self.save(point, temp)
    else:
      time.sleep(0.5)
      i = i + 1
      return self.__uniqueHandle__(sv_screen, point, i)

  def __countReactSize__(self, screen, point, zoom):
    cv_scr = self.__pl2cv__(screen)
    h, w = cv_scr.shape[:2]
    x, y = point
    x1 = x - zoom * 50
    y1 = y - zoom * 50
    x2 = x + zoom * 50
    y2 = y + zoom * 50
    x1 = x1 if x1 > 0 else 0
    y1 = y1 if y1 > 0 else 0
    x2 = x2 if x2 < w else w
    y2 = y2 if y2 < h else h
    return (x1, y1, x2, y2)


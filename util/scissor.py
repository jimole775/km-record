from PIL import Image, ImageGrab
from config import config
import cv2 as cv
import numpy as np
import time
# def getCorePoint(self, rect_loc):
#   x1, y1, x2, y2 = rect_loc
#   react_left_y = y2 - y1
#   react_bottom_x = x2 - x1
#   cross = (react_left_y ** 2 + react_bottom_x ** 2) ** 0.5
#   return ((x2 - x1) / 2, cross / 2)

class Scissor:
  def __init__(self):
    self.point = ''
    self.rectLoc = ''
    self.timestamp = ''
    self.img = ''
    self.saveDir = config.ASSETS_PATH + config.OBJECT_NAME
  def cutReact(self, point):
    x, y = point
    self.point = point
    self.rectLoc = (x - 50, y - 50, x + 50, y + 50)
    self.timestamp = time.time()
    self.img = cv.cvtColor(np.array(ImageGrab.grab(self.rectLoc)), cv.COLOR_RGB2BGR)
    return self
  def save(self):
    fileName = str(self.timestamp) + '_' + str(self.point) + '.jpg'
    cv.imwrite(self.saveDir + '\\' + fileName, self.img)
    return self

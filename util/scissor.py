from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np
import time
def getCorePoint(self, rect_loc):
  x1, y1, x2, y2 = rect_loc
  react_left_y = y2 - y1
  react_bottom_x = x2 - x1
  cross = (react_left_y ** 2 + react_bottom_x ** 2) ** 0.5
  return ((x2 - x1) / 2, cross / 2)

class Scissor():
  def cutReact(self, core_point):
    x, y = core_point
    self.core_point = core_point
    self.rect_loc = (x - 50, y - 50, x + 50, y + 50)
    self.timestamp = time.time()
    self.img = cv.cvtColor(np.array(ImageGrab.grab(self.rect_loc)), cv.COLOR_RGB2BGR)
    return self
  def save(self, object_name):
    file_name = str(self.core_point) + '_' + str(self.timestamp) + '.jpg'
    cv.imwrite('.\\objects\\' + object_name + '\\' + file_name, self.img)
    return self

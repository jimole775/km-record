from PIL import Image, ImageGrab
from config import config
from util.scaner import Scaner
from util.mkdir import mkdir
import cv2 as cv
import numpy as np
import time
import threading
assets_dir = config.PROJECT['path'] + config.PROJECT['name'] + '\\shots'
class Scissors:
    def __init__(self):
        mkdir(assets_dir)
        self.scaner = Scaner()

    def cutUniqueReact(self, screen, point, timeStamp):
        cv_screen = self._pl2cv(screen)
        thread = threading.Thread(target=self._uniqueHandle, args=(cv_screen, point, 1, timeStamp,))
        thread.start()

    def cutReact(self, screen, point, zoom=1):
        x1,y1,x2,y2 = self._countReactSize(screen, point, zoom)
        cv_screen = self._pl2cv(screen)
        return cv_screen[y1:y2, x1:x2]

    def cutReactAndSave(self, screen, point, timeStamp):
        temp = self.cutReact(screen, point)
        return self.save(temp, timeStamp)

    def cutScreen(self):
        return ImageGrab.grab()

    def save(self, temp, timeStamp):
        cv_temp = self._pl2cv(temp)
        fileName = str(timeStamp) + '.jpg'
        cv.imwrite(assets_dir + '\\' + fileName, cv_temp)
        return self

    def _pl2cv(self, img):
        if (isinstance(img, Image.Image)):
            return cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
        else:
            return img

    def _uniqueHandle(self, sv_screen, point, i, timeStamp):
        temp = self.cutReact(sv_screen, point, i)
        if self.scaner.hasUniqueTarget(sv_screen, temp) or i == 10:
            self.save(temp, timeStamp)
        else:
            time.sleep(0.5)
            i = i + 1
            return self._uniqueHandle(sv_screen, point, i, timeStamp)

    def _countReactSize(self, screen, point, zoom):
        cv_scr = self._pl2cv(screen)
        h, w = cv_scr.shape[:2]
        x, y = point
        x1 = x - zoom * 100
        y1 = y - zoom * 100
        x2 = x + zoom * 100
        y2 = y + zoom * 100
        x1 = x1 if x1 > 0 else 0
        y1 = y1 if y1 > 0 else 0
        x2 = x2 if x2 < w else w
        y2 = y2 if y2 < h else h
        return (x1, y1, x2, y2)


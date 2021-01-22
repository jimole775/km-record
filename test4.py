from scaner import FindWindow
from locator import Locator
from util.scissors import Scissors
from replay import Replay
import cv2 as cv
import numpy as np
import time
# import matplotlib.pylab as plt
# if __name__ == "__main__":
# wdname 为连连看窗口的名称，必须写完整
wdname = u'OMS外包管理系统 - Google Chrome'
demo = FindWindow(wdname)
loct = Locator()
rep = Replay()
scor = Scissors()
# time.sleep(1)
if demo.hwnd:
    temps = [
      'step-1.jpg', 'step-2.jpg', 'step-3.jpg', 'step-4.jpg', 'step-5.jpg',
      'step-6.jpg', 'step-7.jpg', 'step-8.jpg', 'step-9.jpg', 'step-10.jpg', 'step-11.jpg'
    ]
    loop = 0
    while loop < len(temps):
      window = scor.cutout(demo.position())
      window = cv.cvtColor(np.array(window), cv.COLOR_RGB2BGR) #PIL转cv
      cur_temp = 'assets/%s'%temps[loop]
      max, min = loct.getCoord(window, cur_temp)
      template = cv.imread(cur_temp, 0)
      w, h = template.shape[::-1]
      cv.rectangle(window, min, (min[0] + w, min[1] + h), (0,0,255), 2)
      rep.start(loop, min[0] + 10, min[1] + 10)
      cv.imwrite('res_%s.png'%loop, window)
      time.sleep(1)
      loop = loop + 1
cv.waitKey(0)
cv.destroyAllWindows()

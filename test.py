from findwindow import FindWindow
import cv2 as cv
import numpy as np
# import matplotlib.pylab as plt
# if __name__ == "__main__":
# wdname 为连连看窗口的名称，必须写完整
wdname = u'OMS外包管理系统 - Google Chrome'
demo = FindWindow(wdname)
if demo.hwnd:
  # while True:
    screen = demo.cutScreen()
    img = cv.cvtColor(np.array(screen), cv.COLOR_RGB2BGR) #PIL转cv
    # cv.imshow('imshow', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    # cv.imwrite('gray_test.png', screen)
# demo.start()

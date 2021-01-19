import cv2 as cv
import numpy as np
from PIL import Image
class Locator():
  def getCoord(self, origin, temp_path):
    """初始化"""
    # temp = Image.open(temp_path)
    # temp = 255 * np.array(temp).astype('uint8')
    # temp = cv.cvtColor(np.array(temp), cv.COLOR_RGB2BGR)  # PIL转cv
    # 选择匹配算法
    cv_origin = cv.cvtColor(np.array(origin), cv.COLOR_RGB2BGR)  # PIL转cv
    cv_temp = cv.cvtColor(np.array(cv.imread(temp_path, 0)), cv.COLOR_RGB2BGR) # PIL转cv

    gray_origin = cv.cvtColor(cv_origin, cv.COLOR_BGR2GRAY)
    gray_temp = cv.cvtColor(cv_temp, cv.COLOR_BGR2GRAY)
    # cv.imwrite('res_bg.jpg', bg)
    # cv.imwrite('res_temp.jpg', temp)
    match_method = cv.TM_CCOEFF_NORMED
    # cv2.TM_CCOEFF_NORMED
    res = cv.matchTemplate(gray_origin, gray_temp, match_method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # print(min_val, max_val, min_loc, max_loc)
    return (min_loc, max_loc)

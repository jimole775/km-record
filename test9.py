import cv2
import numpy as np
from matplotlib import pyplot as plt


# 原文：https://www.cnblogs.com/gezhuangzhuang/p/10724769.html
# 原文：https://blog.csdn.net/qq_21840201/article/details/85084621

# 1. 读入原图和模板
img_rgb = cv2.imread('.\\assets\\mario.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('.\\assets\\mario-icon.jpg', 0)
h, w = template.shape[:2]

# 归一化平方差匹配
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8

# 返回res数组矩阵中，值大于0.8的【坐标】，每匹配成功一个元素
# 就把当前元素的坐标，分别填入(['纵坐标'], ['横坐标'])中
loc = np.where(res >= threshold)

# zip：把loc中的所有相同下标的元素，都拼成一个元组，最后返回一个数组[(),()]
# loc[::-1]：取从后向前（相反）的元素，使其结果对应 x, y
# *号表示解压
for pt in zip(*loc[::-1]):
    right_bottom = (pt[0] + w, pt[1] + h)
    print(pt)
    cv2.rectangle(img_rgb, pt, right_bottom, (0, 0, 255), 2)

# 保存处理后的图片
cv2.imwrite('res.png', img_rgb)

# 显示图片 参数：（窗口标识字符串，imread读入的图像）
cv2.imshow("test_image", img_rgb)

# 窗口等待任意键盘按键输入 0为一直等待 其他数字为毫秒数
cv2.waitKey(0)

# 销毁窗口 退出程序
cv2.destroyAllWindows()
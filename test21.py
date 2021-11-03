import cv2
import numpy as np

img = cv2.imread('E:\\py_pro\\opr-record-pc\\assets\\sys_inputs\\win10\\win.png')
# img = cv2.imread('E:\\py_pro\\opr-record-pc\\business\\temp\\shots\\1634547034.368551.jpg')

# conv_img = np.zeros((int(img.shape[0])-2,
#                         int(img.shape[1])-2,
#                         int(img.shape[2])))
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
for i in range(int(img.shape[0])):
    for j in range(int(img.shape[1])):
        img[i][j] = 255 - img[i][j]
        # conv_img[i][j] = img[i][j+1] + img[i+1][j] + img[i+2][j+1] + img[i+1][j+2] - 4*img[i+1][j+1]
cv2.imwrite('conv6.png', img)
def log():
    print('中文')

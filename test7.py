import pytesseract
from PIL import Image
image = Image.open('E:\\automatic\\assets\\whole.png')
content = pytesseract.image_to_string(image)   # 解析图片
print(content)
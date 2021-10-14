# 获取win10系统的dpi(字体缩放比)
import ctypes
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

LOG_PX_X = 88
LOG_PX_Y = 90

user32.SetProcessDPIAware()
hDC = user32.GetDC(0)
hdpi = gdi32.GetDeviceCaps(hDC, LOG_PX_X)
vdpi = gdi32.GetDeviceCaps(hDC, LOG_PX_Y)

print(hdpi, vdpi)
# 判断windows任务栏高度（不可靠，win10专业版获取高宽有误差）
from win32api import GetMonitorInfo, MonitorFromPoint
import win32gui, win32print, win32con

# dpi的差值，比如设置缩放比为 125%，实际的放大程度只有 120%
MISCOUNT_RATE = 0.96

# 显示器信息
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
# 显示器的全屏高宽像素
monitor_area = monitor_info.get("Monitor")
# 显示器的工作区域的高宽像素
work_area = monitor_info.get("Work")

hDC = win32gui.GetDC(0)

# 当前实际的横向分辨率
cur_screen_width = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
# 当前实际的纵向分辨率
cur_screen_height = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)

zoom_screen_width = monitor_area[2]
zoom_screen_height = monitor_area[3]
zoom_work_width = work_area[2]
zoom_work_height = work_area[3]

# 缩放比
zoom = cur_screen_height / zoom_screen_height


task_height = zoom_screen_height * (1 + zoom) - zoom_work_height * (1 + zoom)

print(zoom)

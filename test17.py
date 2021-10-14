# 判断windows任务栏高度（不可靠，win10专业版获取高宽有误差）
from win32api import GetMonitorInfo, MonitorFromPoint
import win32gui, win32print, win32con
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))

# 获取的是根据字体缩放比获取到的高宽，并非当前实际高宽，只是（win10专业版的一个系统，其他的系统不清楚）
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")

hDC = win32gui.GetDC(0)

#当前的横向分辨率
cur_screen_width = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
#当前的纵向分辨率
cur_screen_height = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)

zoom_screen_width = monitor_area[2]
zoom_screen_height = monitor_area[3]
zoom_work_width = work_area[2]
zoom_work_height = work_area[3]

# 缩放比
zoom = (cur_screen_height - zoom_screen_height) / cur_screen_height


task_height = zoom_screen_height * (1 + zoom) - zoom_work_height * (1 + zoom)

print(task_height)

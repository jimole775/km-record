# 判断windows任务栏高度（不可靠，win10专业版获取高宽有误差）
from win32api import GetMonitorInfo, MonitorFromPoint
import win32gui, win32print, win32con

# 缩放前的显示器信息
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
# 缩放前的显示器的全屏高宽像素
monitor_area = monitor_info.get("Monitor")
# 缩放前的显示器的工作区域的高宽像素
work_area = monitor_info.get("Work")

hDC = win32gui.GetDC(0)

# 当前实际的横向分辨率
cur_screen_width = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
# 当前实际的纵向分辨率
cur_screen_height = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)

zoom_screen_width = monitor_area[2]
zoom_screen_height = monitor_area[3]
# work_area[0] # 任务栏在左侧时的宽度
# work_area[1] # 任务栏在上部时的高度
zoom_work_width = work_area[2]
zoom_work_height = work_area[3]

# 缩放比
zoom = cur_screen_height / zoom_screen_height

def get_task_bar_pos():
    task_pos = (0, 0, 0, 0)
    # 任务栏在 “右侧”
    if (zoom_screen_height == zoom_work_height) and (zoom_screen_width != zoom_work_width):
        task_bar_w = (zoom_screen_width - zoom_work_width) * zoom
        task_pos = (cur_screen_width - task_bar_w, 0, cur_screen_width, cur_screen_height)

    # 任务栏在 “底部”
    if (zoom_screen_width == zoom_work_width) and (zoom_screen_height != zoom_work_height):
        task_bar_h = (zoom_screen_height - zoom_work_height) * zoom
        task_pos = (0, cur_screen_height - task_bar_h, cur_screen_width, cur_screen_height)

    # 任务栏在左侧
    if (work_area[0] > 0):
        task_bar_w = work_area[0] * zoom
        task_pos = (0, 0, task_bar_w, cur_screen_height)

    # 任务栏在上部
    if (work_area[1] > 0):
        task_bar_h = work_area[1] * zoom
        task_pos = (0, 0, cur_screen_width, task_bar_h)

    return task_pos

def get_screen_size():
    return (cur_screen_width, cur_screen_height)

# def is_vertical_task_bar():
#     task_bar_width, task_bar_height = get_task_bar_pos()
#     return zoom_screen_height == task_bar_height

# def is_horizontal_task_bar():
#     task_bar_width, task_bar_height = get_task_bar_pos()
#     return zoom_screen_width == task_bar_width

import win32gui, win32print, win32con
hDC = win32gui.GetDC(0)
#横向分辨率
HORZRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
#纵向分辨率
VERTRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
print(HORZRES,VERTRES)

import wx, wx.html2, os, winreg, time, asyncio

class MyBrowser(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, None, -1, "My Frame", size=(300, 300))
        # 这里需要打开所有权限
        self.key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
              r"SOFTWARE\\Microsoft\\Internet Explorer\\Main\\FeatureControl\\FEATURE_BROWSER_EMULATION", 0, winreg.KEY_ALL_ACCESS)
        try:
            # 设置注册表python.exe 值为 11000(IE11)
            winreg.SetValueEx(self.key, 'python.exe', 0, winreg.REG_DWORD, 0x00002af8)
        except:
            # 设置出现错误
            print('error in set value!')
        self.browser = wx.html2.WebView.New(self, style=0)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def loadUrl(self, url):
        self.browser.LoadURL(os.path.realpath(url))

    def OnClose(self, evt):
        print('close')
        # 用完取消注册表设置
        winreg.DeleteValue(self.key, 'python.exe')
        # 关闭打开的注册表
        winreg.CloseKey(self.key)
        evt.Skip()

if __name__ == '__main__':
    app = wx.App()
    frame = MyBrowser()
    # frame.browser.RunScript('window.zxczxvcvxbvb="98765432"')
    # frame.browser.IsAccessToDevToolsEnabled()
    frame.loadUrl(".\\ui\\html\\dist\\index.html")
    # frame.browser.RunScript('document.title="123"')
    # success, result = frame.browser.RunScript("window.asd=123")
    frame.Show()
    app.MainLoop()
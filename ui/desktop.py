from tkinter import *
from tkinter import messagebox
from ui.conf_play import PlayConfigUI
from util.func import apply
import threading
import wx
class Desktop ():
    def __init__ (self):
        self.app = wx.App()
        self.main = Tk()
        self.main.title("OPR")
        self.main.geometry("200x30")
        self.record_events = []
        self.play_events = []
        self.edit_events = []
        self.config_events = []
        self.createIco()
        self.createButton()
        self.createWxThrd()
        self.playConfigUI = PlayConfigUI(parent=None)

    def createWxThrd (self):
        thread = threading.Thread(target=self.app.MainLoop)
        thread.start()

    def record (self):
        self.excuteEventInThread(self.record_events)
        pass

    def play (self):
        self.playConfigUI.regConfirmEvent(self.excuteEventInThread, self.play_events)
        self.playConfigUI.Show()
        pass

    def edit (self):
        self.excuteEventInThread(self.edit_events)
        pass

    def config (self):
        self.excuteEventInThread(self.config_events)
        pass

    def excuteEventInThread (self, event):
        thread = self.createThread(self.callInjectedFunction, event)
        thread.start()

    def createThread (self, fn, param):
        return threading.Thread(target=fn, args=(param,))

    # 自动调用注入函数队列
    def callInjectedFunction (self, events):
        print(events)
        for event in events:
            e_instance = event[0]
            e_paramets = event[1:]
            apply(e_instance, e_paramets)

    def createIco (self):
        self.ico_record = PhotoImage(file='assets/record.png')
        self.ico_play = PhotoImage(file='assets/play.png')
        self.ico_edit = PhotoImage(file='assets/edit.png')
        self.ico_config = PhotoImage(file='assets/config.png')

    def helloCallBack(self, text):
        messagebox.showinfo("Hello Python", text)

    def createButton (self):
        b_record = Button(self.main, text = "录制", command = self.record)
        b_play = Button(self.main, text = "播放", command = self.play)
        b_edit = Button(self.main, text = "编辑", command = self.edit)
        b_config = Button(self.main, text = "配置", command = self.config)
        # 1，录制项目；2，播放项目；3，编辑项目；4，配置快捷键；5，退出
        b_play['image'] = self.ico_play
        b_edit['image'] = self.ico_edit
        b_record['image'] = self.ico_record
        b_config['image'] = self.ico_config
        b_record.grid(row=0, column=0)
        b_play.grid(row=0, column=1)
        b_edit.grid(row=0, column=2)
        b_config.grid(row=0, column=3, sticky='E')

    ## 录制
    "【弹窗】"
    "项目名："
    "存放路径："

    ## 播放
    "【弹窗】"
    "选择资源"

    ## 编辑

    ## 快捷键
    "【弹窗】"
    "录制=>开始，暂停，结束..."
    "播放=>开始，暂停，结束..."

    ## 注册功能函数
    def registerFunction (self, fn_type, fn_tuple):
        if type(fn_type) == str and type(fn_tuple) == tuple:
            self_event_stack = eval('self.' + fn_type + '_events')
            self_event_stack.append(fn_tuple)

    def open (self):
        ## 挂载
        self.main.mainloop()

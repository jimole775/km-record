from tkinter import *
from tkinter import messagebox
from ui.play.config import PConfigUI
from ui.record.config import RCConfigUI
from util.func import apply
from states.state_desktop import StateDesktop

import threading
import wx
class Desktop ():
    state = StateDesktop()
    def __init__(self):
        self.app = wx.App()
        self.main = Tk()
        self.main.title("OPR")
        self.main.geometry("200x30")
        self.play_events = []
        self.edit_events = []
        self.config_events = []
        self.record_events = []
        self.createIco()
        self.createButton()
        self.PConfigUI = PConfigUI(parent=None)
        self.RCConfigUI = RCConfigUI(parent=None)
        Desktop.state.subscribe('active', self.active_callback)
    
    def active_callback (self, val):
        if (val == 0):
            self.win_show()
        if (val == 0):
            self.win_hide()
        if (val == 0):
            self.win_destroy()
            pass
    
    def createWxThrd (self):
        thread = threading.Thread(target=self.app.MainLoop)
        thread.start()
        pass
    def record (self):
        self.PConfigUI.regConfirmEvent(self.excuteEventInThread, self.record_events)
        self.PConfigUI.Show()
        self.win_hide()
        pass
    def play (self):
        self.PConfigUI.regConfirmEvent(self.excuteEventInThread, self.play_events)
        self.PConfigUI.Show()
        self.win_hide()
        pass
    def edit (self):
        self.excuteEventInThread(self.edit_events)
        self.win_hide()
        pass
    def config (self):
        self.excuteEventInThread(self.config_events)
        self.win_hide()
        pass
    def excuteEventInThread (self, event):
        thread = self.createThread(self.callInjectedFunction, event)
        thread.start()
        pass
    def createThread (self, fn, param):
        return threading.Thread(target=fn, args=(param,))
        pass
    def callInjectedFunction (self, events):
        print(events)
        for event in events:
            e_instance = event[0]
            e_paramets = event[1:]
            apply(e_instance, e_paramets)

        pass
    def createIco (self):
        self.ico_record = PhotoImage(file='assets/record.png')
        self.ico_play = PhotoImage(file='assets/play.png')
        self.ico_edit = PhotoImage(file='assets/edit.png')
        self.ico_config = PhotoImage(file='assets/config.png')
        pass
    def createButton (self):
        b_play = Button(self.main, text="播放", command=self.play)
        b_edit = Button(self.main, text="编辑", command=self.edit)
        b_record = Button(self.main, text="录制", command=self.record)
        b_config = Button(self.main, text="配置", command=self.config)

        b_play['image'] = self.ico_play
        b_edit['image'] = self.ico_edit
        b_record['image'] = self.ico_record
        b_config['image'] = self.ico_config

        b_record.grid(row=0, column=0)
        b_play.grid(row=0, column=1)
        b_edit.grid(row=0, column=2)
        b_config.grid(row=0, column=3, sticky='E')

        pass
    def helloCallback (self, text):
        messagebox.showinfo('Hello Python', text)
        pass
    def win_destroy (self):
        self.main.destroy()
        pass
    def win_hide (self):
        self.main.withdraw()
        pass
    def win_show (self):
        self.main.update()
        self.main.deiconify()
        pass
    def registerFunction (self, fn_type, fn_tuple):
        if type(fn_type) == str and type(fn_tuple) == tuple:
            self_event_stack = eval('self.' + fn_type + '_events')
            self_event_stack.append(fn_tuple)
        pass

    def open (self):
        self.main.mainloop()
        pass
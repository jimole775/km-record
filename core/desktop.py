from tkinter import *
from tkinter import messagebox
import threading
class Desktop ():
    def __init__ (self):
        self.main = Tk()
        self.main.title("OPR")
        self.main.geometry("200x30")
        self.record_events = []
        self.play_events = []
        self.edit_events = []
        self.config_events = []
        self.createIco()
        self.createButton()

    def record (self):
        thread = threading.Thread(target=self.callInjectedFunction, args=(self.record_events,))
        thread.start()
        self.helloCallBack('录制功能调用成功！')
        pass

    def play (self):
        thread = threading.Thread(target=self.callInjectedFunction, args=(self.play_events,))
        thread.start()
        pass
    def edit (self):
        thread = threading.Thread(target=self.callInjectedFunction, args=(self.edit_events,))
        thread.start()
        pass

    def config (self):
        thread = threading.Thread(target=self.callInjectedFunction, args=(self.config_events,))
        thread.start()
        pass

    def callInjectedFunction (self, events):
        for event in events:
            e_instance = event[0]
            e_paramets = event[1:]
            if callable(e_instance):
                param_dict = {}
                param_cont = e_instance.__code__.co_argcount
                if param_cont > 0:
                    param_names = e_instance.__code__.co_varnames[0:param_cont]
                    i = 0
                    for p_name in param_names:
                        param_dict[p_name] = e_paramets[i]
                        i = i + 1
                e_instance.__call__(**param_dict)

        pass
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
            event_stack = eval('self.' + fn_type + '_events')
            event_stack.append(fn_tuple)

    ## 退出
    def open (self):
        ## 挂载
        self.main.mainloop()

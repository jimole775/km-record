# 选择项目路径和项目名

# 是否随机文本：？输入的文本会在后面加上随机文本

# 热键配置
## 开始录制：F1
## 暂停录制：F2
## 继续录制：F3
## 取消录制：F4
## 重新录制：F5
## 退出：F8

# 'match': {
#     'times': 10, # 在执行click事件的时候，是否需要匹配有没有目标元素
#     'interval': 0.5, # 在执行click事件的时候，是否需要匹配有没有目标元素
# },
# 'project': {
#     'name': 'temp', # 录制的项目名，默认为temp
#     'path': '.\\business\\' # 录制项目的存储路径
# },
# 'hotkey': {
#     'play': {
#         u'开始': 'F1',
#         u'循环': 'F2',
#         u'暂停': 'F3',
#         u'继续': 'F4',
#         u'结束': 'F5',
#     },
#     'record': {
#         u'开始': 'F1',
#         u'暂停': 'F2',
#         u'继续': 'F3',
#         u'结束': 'F4',
#     }
# }

# 开始录制

from tkinter import *
from tkinter import messagebox
from util.func import apply
import threading
class RecordConfig ():
    def __init__ (self):
        print('RecordConfig init')
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
        self.excuteEventInThread(self.record_events)
        pass

    def play (self):
        self.excuteEventInThread(self.play_events)
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
        for event in events:
            e_instance = event[0]
            e_paramets = event[1:]
            call(e_instance, e_paramets)
            # if callable(e_instance):
            #     param_dict = {}
            #     # 获取函数的参数数量
            #     param_cont = e_instance.__code__.co_argcount
            #     if param_cont > 0:
            #         # 获取函数的参数列表
            #         param_names = e_instance.__code__.co_varnames[0:param_cont]
            #         i = 0
            #         for p_name in param_names:
            #             # 把参数列表和参数值拼成字典
            #             param_dict[p_name] = e_paramets[i]
            #             i = i + 1
            #     e_instance.__call__(**param_dict)

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

    def open (self):
        ## 挂载
        self.main.mainloop()

from tkinter import *
from tkinter import messagebox
class Desktop ():
    def __init__ (self):
        self.main = Tk()
        self.main.title("OPR")
        self.main.geometry("200x30")
        self.create_ico()
        self.create_button()

    def create_ico (self):
        self.ico_record = PhotoImage(file='assets/record.png')
        self.ico_play = PhotoImage(file='assets/play.png')
        self.ico_edit = PhotoImage(file='assets/edit.png')
        self.ico_config = PhotoImage(file='assets/config.png')


    def helloCallBack(self):
        messagebox.showinfo("Hello Python", "asdasd")


    def create_button (self):
        b_record = Button(self.main, text = "录制", command = self.helloCallBack)
        b_play = Button(self.main, text = "播放", command = self.helloCallBack)
        b_edit = Button(self.main, text = "编辑", command = self.helloCallBack)
        b_config = Button(self.main, text = "配置", command = self.helloCallBack)
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

    ## 退出
    def mount (self):
        ## 挂载
        self.main.mainloop()

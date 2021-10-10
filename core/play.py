# import pyautogui as gui
# import numpy as np
# import cv2 as cv
import os
import re
import time
import threading
import json
import pynput
import ctypes


from config import config
from util.keyboard import get_keyboard_key
from util.scaner import Scaner
from util.scissors import Scissors
# from core.mouse import MouseController
from core.keyboard import KeyboardController
from core.controller import createController

# 处理windows系统对于坐标读取的误差问题
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

abbr = config.ABBR
assets_dir = config.PROJECT['path'] + config.PROJECT['name']

random_type_key = get_keyboard_key(config.CMD['random_type'])

m_handler = pynput.mouse.Controller()
k_handler = pynput.keyboard.Controller()
class Play:
    def __init__(self):
        self.play_type = 'once'
        self.pause_sign = False
        self.stop_sign = False
        self.step = 0
        self.step_at_pause = 0
        self.scissors = Scissors()
        self.scaner = Scaner()
        self.k_controller = KeyboardController()
        # self.step_items = self._getSteps()
        if config.MATCH: # 是否启用视觉匹配
            print('config.MATCH:', config.MATCH)
            self.check_i = config.MATCH['times']
            self.check_max = config.MATCH['times']
            self.interval = config.MATCH['interval']
        else:
            self.check_i = 0
            self.check_max = 0
            self.interval = 0.5
        pass

    def _getNextTime(self, cur_index, file_list):
        if cur_index < len(file_list) - 1:
            nextFile = file_list[cur_index + 1]
        else:
            nextFile = file_list[cur_index]
        return re.search(r'^\d*?\.?\d*?(?=\_)', nextFile).group()

    def _runHandler(self):
        opr_file = open(assets_dir + '\\index.log', 'r')
        if self.step > 0:
            opr_file.seek(self.step)
        line = opr_file.readline()
        self.step = opr_file.tell()
        while len(line) > 0:
            step_item = json.loads(line)
            """
            # todo 需要区分事件类型：
            # 包括 点击，拖拽，按键，组合键
            """
            # 鼠标事件
            if step_item[abbr['type']] == abbr['mouse']:
                loc = step_item[abbr['loc']]
                m_handler.position = (loc[0], loc[1])
                if step_item[abbr['mouse_event']] == abbr['press']:
                    m_handler.press(pynput.mouse.Button.left)

                if step_item[abbr['mouse_event']] == abbr['release']:
                    if config.MATCH:
                        screen = self.scissors.cutScreen()
                        shot_name = step_item[abbr['time']]
                        shot_img = assets_dir + '\\shots\\' + shot_name + '.jpg'
                        if self.scaner.hasUniqueTarget(screen, shot_img) or self.check_i == 0:
                            self._resetCheckTimes()
                            m_handler.release(pynput.mouse.Button.left)
                        else:
                            self._checkReduce()
                    else:
                        m_handler.release(pynput.mouse.Button.left)
                if step_item[abbr['mouse_event']] == abbr['scroll']:
                    m_handler.scroll(loc[2], loc[3])

            # 键盘事件
            if step_item[abbr['type']] == abbr['keyboard']:
                key_code = step_item[abbr['key']]
                self._kb_type(key_code)
            if (self.pause_sign or self.stop_sign):
                break
            line = opr_file.readline()
            if len(line) > 0:
                o_item = step_item
                n_item = json.loads(line)
                time.sleep(float(n_item['i']) - float(o_item['i']))
            self.step = opr_file.tell()
        opr_file.close()

    """
    # todo 使用 press 和 release 来模拟type，因为keyboard.type()方法对code的输入支持一般
    """
    def _kb_type(self, keys):
        kb_key = get_keyboard_key(keys)
        if (kb_key == random_type_key):
            self._rundom_type()
            pass
        if type(kb_key) == list:
            for item in kb_key:
                k_handler.press(item)
            l = len(kb_key)
            while(l > 0):
                l = l - 1
                item = kb_key[l]
                k_handler.release(item)
        else:
            k_handler.press(kb_key)
            k_handler.release(kb_key)
        pass

    # 输入随机数
    def _rundom_type():
        k_handler.type(time.time())

    # 计算匹配消耗的时间
    def _checkedSeconds(self):
        return (self.check_max - self.check_i) * self.interval

    # def _domoves(self, step_item):
    #     x, y = step_item['loc']
    #     gui.moveTo(x, y)
    #     time.sleep(self.interval)

    # def _doclick(self, step_item):
    #     x, y = step_item['loc']
    #     gui.moveTo(x, y)
    #     gui.click()

    def _waiting(self, t_remian):
        if t_remian > self.interval:
            time.sleep(t_remian)
        else:
            time.sleep(self.interval)

    def _checkReduce(self):
        print('check_i:', self.check_i)
        self.check_i = self.check_i - 1

    def _resetCheckTimes(self):
        if config.MATCH:
          self.check_i = config.MATCH['times']
        else:
          self.check_i = 0

    def _stepGrow(self):
        self.step = self.step + 1
        print('step:', self.step)

    def _doplay(self):
        if self.play_type == 'once':
            self.once()
        if self.play_type == 'repeat':
            self.repeat()

    def start(self, type = 'once'):
        self.play_type = type
        self.stop_sign = False
        self.pause_sign = False
        self.step = 0
        self._doplay()

    def stop(self):
        self.stop_sign = True
        print('stop play')
        pass

    def pause(self):
        self.pause_sign = True
        self.step_at_pause = self.step
        print('pause:', self.step)
        pass

    def continues(self):
        self.stop_sign = False
        self.pause_sign = False
        self.step = self.step_at_pause
        print('continue:', self.step)
        self._doplay()
        pass

    def once(self):
        self.play_type = 'once'
        self._runHandler()

    def repeat(self):
        self.play_type = 'repeat'
        while self.pause_sign == False and self.stop_sign == False:
            self._runHandler()
            self.step = 0

    def run (self):
        self._createThread(self._keyboardEvent)

    def _createThread (self, event):
        thread = threading.Thread(target=event)
        thread.start()

    def _keyboardEvent (self):
        ctrl = createController(Play)()
        self.k_controller.bindExecution(ctrl.execution)
        self.k_controller.active()

    def _getSteps(self):
        i = 0
        step_items = []
        if config.MATCH: # 是否启用视觉匹配
            match_pic_dir = assets_dir + '\\shots'
            file_list = os.listdir(match_pic_dir)
            for file_name in file_list:
                timestamp = re.search(r'^\d*?\.?\d*?(?=\_)', file_name).group()
                loc = eval(re.search(r'\(\d*?, \d*?\)', file_name).group())
                insert = re.search(r'insert', file_name)
                nextTime = self._getNextTime(i, file_list)
                step_items.append({
                    'loc': loc,
                    'insert': insert, # 判断是否是手动插入帧
                    'shot': assets_dir + '\\' + file_name,
                    'sleep': float(nextTime) - float(timestamp),
                })
                i = i + 1
        else: # 直接从log中拉取操作记录
            opr_file = open(assets_dir + '\\index.log', 'r')
            line = opr_file.readline()
            item = json.loads(line)
            step_items.append({
                'loc': item.loc,
                'shot': None
                # 'sleep': float(nextTime) - float(timestamp),
            })
        return step_items

import pyautogui as gui
import numpy as np
import cv2 as cv
import os
import re
import time
import threading
from config import config
from util.scaner import Scaner
from util.scissors import Scissors
# from core.mouse import MouseController
from core.keyboard import KeyboardController
from core.controller import createController

assets_dir = config.PROJECT['path'] + config.PROJECT['name']

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
        self.step_items = self._getSteps()
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
        while self.step < len(self.step_items):
            if (self.pause_sign or self.stop_sign):
                break
            step_item = self.step_items[self.step]
            """
            # 录制时截取的图片, 是鼠标移动到目标位置，点击之后的,
            # 那么, 需要准确的记录出移动到目的地之后的滞留时间
            """
            self._domoves(step_item)
            if config.MATCH:
                screen = self.scissors.cutScreen()
                temp = step_item['file']
                if self.scaner.hasUniqueTarget(screen, temp) or self.check_i == 0:
                    self._resetCheckTimes()
                    self._doclick(step_item)
                    self._stepGrow()
                    self._waiting(step_item['sleep'] - self._checkedSeconds())
                else:
                    self._checkReduce()
                    self._waiting(self.interval)
            else:
                self._doclick(step_item)
                self._stepGrow()
                self._waiting(self.interval)

    # 计算匹配消耗的时间
    def _checkedSeconds(self):
        return (self.check_max - self.check_i) * self.interval

    def _domoves(self, step_item):
        x, y = step_item['loc']
        gui.moveTo(x, y)
        time.sleep(self.interval)

    def _doclick(self, step_item):
        x, y = step_item['loc']
        gui.moveTo(x, y)
        gui.click()

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
        self.k_controller.start()

    def _getSteps(self):
        i = 0
        step_items = []
        if config.MATCH: # 是否启用视觉匹配
            match_pic_dir = assets_dir + '\\matchs'
            file_list = os.listdir(assets_dir)
            for file_name in file_list:
                timestamp = re.search(r'^\d*?\.?\d*?(?=\_)', file_name).group()
                loc = eval(re.search(r'\(\d*?, \d*?\)', file_name).group())
                insert = re.search(r'insert', file_name)
                nextTime = self._getNextTime(i, file_list)
                step_items.append({
                    'loc': loc,
                    'insert': insert,
                    'file': assets_dir + '\\' + file_name,
                    'sleep': float(nextTime) - float(timestamp),
                })
                i = i + 1
        else: # 直接从log中拉取操作记录
            
            print('sss')
        return step_items

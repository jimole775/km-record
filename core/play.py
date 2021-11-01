# import pyautogui as gui
# import numpy as np
# import cv2 as cv
# import os
import re
import time
import threading
import json
import pynput
import ctypes

from util.sys import get_sys_language
from config import config
from util.keyboard import get_keyboard_key
from util.scaner import Scaner
from util.scissors import Scissors
from core.keyboard import KeyboardController
from core.controller import createController

# 处理windows系统对于坐标读取的误差问题
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

g = {
    'abbr': config.ABBR,
    'assets_dir': config.PROJECT['path'] + config.PROJECT['name'],
    'random_type_key': get_keyboard_key(config.CMD['random_type']['key']),
    'm_handler': pynput.mouse.Controller(),
    'k_handler': pynput.keyboard.Controller(),
    'sys_language': get_sys_language(),
}

# 输入随机数
def _rundom_type():
    r_t = time.time()
    g['k_handler'].type(str(r_t))

def _chang_input_language():
    kb_key = get_keyboard_key('shift')
    g['k_handler'].press(kb_key)
    g['k_handler'].release(kb_key)
    time.sleep(0.2)
    g['sys_language'] = get_sys_language()

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

    def _runHandler(self):
        opr_file = open(g['assets_dir'] + '\\index.log', 'r')
        self._sync_pionter(opr_file)
        line = self._get_opr_line(opr_file)
        while len(line) > 0:
            step_item = json.loads(line)
            # 鼠标事件
            if step_item[g['abbr']['type']] == g['abbr']['mouse']:
                self._run_mouse_events(step_item)

            # 键盘事件
            if step_item[g['abbr']['type']] == g['abbr']['keyboard']:
                self._kb_type(step_item)

            if (self.pause_sign or self.stop_sign):
                break

            line = self._prepare_next(opr_file, step_item)
        opr_file.close()
        pass

    def _sync_pionter(self, opr_file):
        if self.step > 0:
            opr_file.seek(self.step)
        pass

    def _prepare_next(self, opr_file, step_item):
        line = self._get_opr_line(opr_file)
        if len(line) > 0:
            o_item = step_item
            n_item = json.loads(line)
            time.sleep(float(n_item['i']) - float(o_item['i']))
        return line

    def _get_opr_line(self, opr_file):
        line = opr_file.readline()
        self._step_grow(opr_file)
        return line

    def _run_mouse_events(self, step_item):
        loc = step_item[g['abbr']['loc']]
        g['m_handler'].position = (loc[0], loc[1])
        if step_item[g['abbr']['mouse_event']] == g['abbr']['press']:
            g['m_handler'].press(pynput.mouse.Button.left)

        if step_item[g['abbr']['mouse_event']] == g['abbr']['release']:
            if config.MATCH:
                screen = self.scissors.cutScreen()
                shot_name = step_item[g['abbr']['time']]
                shot_img = g['assets_dir'] + '\\shots\\' + shot_name + '.jpg'
                if self.scaner.hasUniqueTarget(screen, shot_img) or self.check_i == 0:
                    self._resetCheckTimes()
                    g['m_handler'].release(pynput.mouse.Button.left)
                else:
                    self._checkReduce()
            else:
                g['m_handler'].release(pynput.mouse.Button.left)
        if step_item[g['abbr']['mouse_event']] == g['abbr']['scroll']:
            g['m_handler'].scroll(loc[2], loc[3])
        pass

    def _sync_input_language(self, step_item):
        cur_step_il = step_item[g['abbr']['input_language']]
        if (g['sys_language'] != cur_step_il):
            _chang_input_language()

    def _kb_type(self, step_item):
        key_code = step_item[g['abbr']['key']]
        kb_key = get_keyboard_key(key_code)
        self._sync_input_language(step_item)
        if (kb_key == g['random_type_key']):
            _rundom_type()
            return
        if type(kb_key) == list:
            for item in kb_key:
                # print('comb press:', item)
                g['k_handler'].press(item)
            l = len(kb_key)
            while(l > 0):
                l = l - 1
                item = kb_key[l]
                # print('comb release:', item)
                g['k_handler'].release(item)
        else:
            # print('press:', kb_key)
            g['k_handler'].press(kb_key)
            # print('release:', kb_key)
            g['k_handler'].release(kb_key)
        pass

    # 计算匹配消耗的时间
    def _checkedSeconds(self):
        return (self.check_max - self.check_i) * self.interval

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

    def _step_grow(self, opr_file):
        self.step = opr_file.tell()

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
        self.k_controller.stop()
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
        self.stop()

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

import json
import time
import threading
from core.mouse import MouseController
from core.keyboard import KeyboardController
from config import config
from core.controller import createController
from util.keyboard import get_key_char
from util.scissors import Scissors
from util.times import skin_time

ABBR = config.ABBR
ASSETS_DIR = config.PROJECT['path'] + config.PROJECT['name']
INPUT_SYSTEM = 'ms' # 当前输入法，一般就是讯飞，搜狗，微软，五笔

class Record ():
    work = False
    scissors = Scissors()
    m_controller = MouseController()
    k_controller = KeyboardController()
    def __init__ (self):
        pass
    def _keyboardEvent (self):
        ctrl = createController(Record)()
        Record.k_controller.registe({
          'text': self._event_kb_text,
          'press': self._event_kb_press,
          'release': self._event_kb_release,
        })
        Record.k_controller.bindExecution(ctrl.execution)
        Record.k_controller.active()

    def _createThread (self, event):
        thread = threading.Thread(target=event)
        thread.start()

    def _mouseEvent (self):
        Record.m_controller.registe({
          'drag': self._event_ms_drag,
          'move': self._event_ms_move,
          'press': self._event_ms_press,
          'scroll': self._event_ms_scroll,
          'release': self._event_ms_release
        })
        Record.m_controller.active()

    def _event_ms_drag (self, event_info):
        self._record_ms_behavior('drag', event_info)
        pass

    def _event_ms_move (self, event_info):
        self._record_ms_behavior('move', event_info)
        pass

    def _event_ms_scroll (self, event_info):
        self._record_ms_behavior('scroll', event_info)
        pass

    def _event_ms_press (self, event_info):
        self._record_ms_behavior('press', event_info)
        pass

    def _event_ms_release (self, event_info):
        self._screen_shot(event_info)
        self._record_ms_behavior('release', event_info)
        pass

    def _event_kb_text (self, event_info):
        self._record_kb_behavior('text', event_info)
        pass

    def _event_kb_press (self, event_info):
        self._record_kb_behavior('press', event_info)
        pass

    def _event_kb_release (self, event_info):
        self._record_kb_behavior('release', event_info)
        pass

    def start (self):
        Record.work = True
        pass

    def run (self):
        self._createThread(self._keyboardEvent)
        self._createThread(self._mouseEvent)

    def stop (self):
        Record.k_controller.stop()
        Record.m_controller.stop()

    # 记录键盘操作
    # event_info: 'key', 'time_stamp', 'sys_language'
    def _record_kb_behavior (self, keyboard_event, event_info):
        key = event_info['key']
        if keyboard_event != 'text':
            key = get_key_char(key)
        if Record.work == True:
            data = {
                ABBR['type']: ABBR['keyboard'],
                ABBR['time']: event_info['time_stamp'],
                ABBR['key']: key,
                ABBR['keyboard_event']: ABBR[keyboard_event],
                ABBR['input_language']: event_info['sys_language']
            }
            self._write(data)
        pass

    # 记录鼠标操作
    # event_info: 'loc', 'time_stamp'
    def _record_ms_behavior (self, mouse_event, event_info):
        if Record.work == True:
            data = {
                ABBR['type']: ABBR['mouse'],
                ABBR['loc']: event_info['loc'],
                ABBR['time']: event_info['time_stamp'],
                ABBR['mouse_event']: ABBR[mouse_event]
            }
            self._write(data)
        pass

    def _write (self, val):
        str = json.dumps(val)
        r_file = open(ASSETS_DIR + '/index.log', 'a+')
        r_file.write(str + '\n')
        r_file.close()

    def _screen_shot (self, event_info):
        if config.MATCH and Record.work == True:
            screen = Record.scissors.cutScreen()
            Record.scissors.cutUniqueReact(screen, event_info['loc'], event_info['time_stamp'])

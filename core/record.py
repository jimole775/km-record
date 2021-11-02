import json
import time
import threading
from core.mouse import MouseController
from core.keyboard import KeyboardController
from config import config
from core.controller import createController
from util.keyboard import get_key_char
from util.scissors import Scissors
from util.times import cute_head
from util.sys import get_sys_language

class Record ():

    work = False
    scissors = Scissors()
    m_controller = MouseController()
    k_controller = KeyboardController()
    sys_language = get_sys_language() # 当前中英文

    ABBR = config.ABBR
    ASSETS_DIR = config.PROJECT['path'] + config.PROJECT['name']
    INPUT_SYSTEM = 'ms' # 当前输入法，一般就是讯飞，搜狗，微软，五笔
    LANG_TRANS_KEY = 'shift' # 中英切换的键

    def __init__ (self):
        pass

    def _keyboardEvent (self):
        ctrl = createController(Record)()
        Record.k_controller.registe({
          'press': self._event_kb_press,
          'release': self._record_kb_behavior
        })
        Record.k_controller.bindExecution(ctrl.execution)
        Record.k_controller.active()

    def _createThread (self, event):
        thread = threading.Thread(target=event)
        thread.start()

    def _mouseEvent (self):
        Record.m_controller.registe({
          'drag': self._event_ms_drag,
          'drag_move': self._event_ms_drag_move,
          'press': self._event_ms_press,
          'scroll': self._event_ms_scroll,
          'release': self._event_ms_release
        })
        Record.m_controller.active()

    def _event_ms_drag (self, loc, timeStamp):
        self._record_ms_behavior(Record.ABBR['drag'], loc, timeStamp)
        pass

    def _event_ms_drag_move (self, loc, timeStamp):
        self._record_ms_behavior(Record.ABBR['drag_move'], loc, timeStamp)
        pass

    def _event_ms_scroll (self, loc, timeStamp):
        self._record_ms_behavior(Record.ABBR['scroll'], loc, timeStamp)
        pass

    def _event_ms_press (self, loc, timeStamp):
        self._record_ms_behavior(Record.ABBR['press'], loc, timeStamp)
        pass

    def _event_ms_release (self, loc, timeStamp):
        self._screen_shot(loc, timeStamp)
        self._record_ms_behavior(Record.ABBR['release'], loc, timeStamp)
        pass

    def _event_kb_press (self, key):
        # key_char = get_key_char(key)
        # print('press key_char:', key_char)
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

    def _record_kb_behavior (self, key, stamp):
        key_char = get_key_char(key)
        if Record.LANG_TRANS_KEY == key_char:
            time.sleep(0.25)
            Record.sys_language = get_sys_language()
        if Record.work == True:
            data = {
                Record.ABBR['type']: Record.ABBR['keyboard'],
                Record.ABBR['time']: cute_head(stamp),
                Record.ABBR['key']: key_char,
                Record.ABBR['input_language']: Record.sys_language
            }
            self._write(data)
        pass

    # 记录操作
    def _record_ms_behavior (self, event, loc, stamp):
        if Record.work == True:
            data = {
                Record.ABBR['type']: Record.ABBR['mouse'],
                Record.ABBR['loc']: loc,
                Record.ABBR['time']: cute_head(stamp),
                Record.ABBR['mouse_event']: event
            }
            self._write(data)
        pass

    def _write (self, val):
        str = json.dumps(val)
        r_file = open(Record.ASSETS_DIR + '/index.log', 'a+')
        r_file.write(str + '\n')
        r_file.close()

    def _screen_shot (self, loc, timeStamp):
        if config.MATCH and Record.work == True:
            screen = Record.scissors.cutScreen()
            Record.scissors.cutUniqueReact(screen, loc, cute_head(timeStamp))

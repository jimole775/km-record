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
from util.sys import isCnType, isEnType

abbr = config.ABBR
assets_dir = config.PROJECT['path'] + config.PROJECT['name']

class Record ():
    work = False
    input_language = 'en' # 当前中英文
    input_system = 'ms' # 当前输入法，一般就是讯飞，搜狗，微软，五笔
    def __init__ (self):
        self.scissors = Scissors()
        self.k_controller = KeyboardController()
        self.m_controller = MouseController()
        if isCnType():
            Record.input_language = 'cn'
        else:
            Record.input_language = 'en'
        pass

    def _createThread (self, event):
        thread = threading.Thread(target=event)
        thread.start()

    def _keyboardEvent (self):
        ctrl = createController(Record)()
        self.k_controller.registe({
          'press': self._event_kb_press,
          'release': self._record_kb_behavior
        })
        self.k_controller.bindExecution(ctrl.execution)
        self.k_controller.active()

    def _mouseEvent (self):
        self.m_controller.registe({
          'drag': self._event_ms_drag,
          'drag_move': self._event_ms_drag_move,
          'press': self._event_ms_press,
          'scroll': self._event_ms_scroll,
          'release': self._event_ms_release
        })
        self.m_controller.active()

    def _event_ms_drag(self, loc, timeStamp):
        self._record_ms_behavior(abbr['drag'], loc, timeStamp)
        pass

    def _event_ms_drag_move(self, loc, timeStamp):
        self._record_ms_behavior(abbr['drag_move'], loc, timeStamp)
        pass

    def _event_ms_scroll(self, loc, timeStamp):
        self._record_ms_behavior(abbr['scroll'], loc, timeStamp)
        pass

    def _event_ms_press(self, loc, timeStamp):
        self._record_ms_behavior(abbr['press'], loc, timeStamp)
        pass

    def _event_ms_release(self, loc, timeStamp):
        self._screen_shot(loc, timeStamp)
        self._record_ms_behavior(abbr['release'], loc, timeStamp)
        pass

    def _event_kb_press():
        pass

    def start(self):
        Record.work = True
        pass

    def run (self):
        self._createThread(self._keyboardEvent)
        self._createThread(self._mouseEvent)

    def stop (self):
        self.k_controller.stop()
        self.m_controller.stop()

    def _record_kb_behavior(self, key, stamp):
        key_char = get_key_char(key)
        if 'shift' in key_char:
            if isCnType():
                Record.input_language = 'cn'
            else:
                Record.input_language = 'en'
        if Record.work == True:
            data = {
                abbr['type']: abbr['keyboard'],
                abbr['time']: cute_head(stamp),
                abbr['key']: key_char,
                abbr['input_language']: Record.input_language
            }
            self._write(data)
        pass

    # 记录操作
    def _record_ms_behavior(self, event, loc, stamp):
        if Record.work == True:
            data = {
                abbr['type']: abbr['mouse'],
                abbr['loc']: loc,
                abbr['time']: cute_head(stamp),
                abbr['mouse_event']: event
            }
            self._write(data)
        pass

    def _write(self, val):
        str = json.dumps(val)
        r_file = open(assets_dir + '/index.log', 'a+')
        r_file.write(str + '\n')
        r_file.close()

    def _screen_shot(self, loc, timeStamp):
        if config.MATCH and Record.work == True:
            screen = self.scissors.cutScreen()
            self.scissors.cutUniqueReact(screen, loc, cute_head(timeStamp))

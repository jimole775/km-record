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

class Record ():

    work = False
    scissors = Scissors()
    m_controller = MouseController()
    k_controller = KeyboardController()

    ABBR = config.ABBR
    ASSETS_DIR = config.PROJECT['path'] + config.PROJECT['name']
    INPUT_SYSTEM = 'ms' # 当前输入法，一般就是讯飞，搜狗，微软，五笔

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
          'drag_move': self._event_ms_drag_move,
          'press': self._event_ms_press,
          'scroll': self._event_ms_scroll,
          'release': self._event_ms_release
        })
        Record.m_controller.active()

    def _event_ms_drag (self, loc, stamp):
        self._record_ms_behavior(Record.ABBR['drag'], loc, stamp)
        pass

    def _event_ms_drag_move (self, loc, stamp):
        self._record_ms_behavior(Record.ABBR['drag_move'], loc, stamp)
        pass

    def _event_ms_scroll (self, loc, stamp):
        self._record_ms_behavior(Record.ABBR['scroll'], loc, stamp)
        pass

    def _event_ms_press (self, loc, stamp):
        self._record_ms_behavior(Record.ABBR['press'], loc, stamp)
        pass

    def _event_ms_release (self, loc, stamp):
        self._screen_shot(loc, stamp)
        self._record_ms_behavior(Record.ABBR['release'], loc, stamp)
        pass

    def _event_kb_text (self, text, stamp, lang):
        self._record_kb_behavior(text, 'text', stamp, lang)
        pass

    def _event_kb_press (self, key, stamp, lang):
        self._record_kb_behavior(key, 'press', stamp, lang)
        pass

    def _event_kb_release (self, key, stamp, lang):
        self._record_kb_behavior(key, 'release', stamp, lang)
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
    def _record_kb_behavior (self, key, keyboard_event, stamp, lang):
        if keyboard_event != 'text':
            key = get_key_char(key)
        if Record.work == True:
            data = {
                Record.ABBR['type']: Record.ABBR['keyboard'],
                Record.ABBR['time']: skin_time(stamp),
                Record.ABBR['key']: key,
                Record.ABBR['keyboard_event']: Record.ABBR[keyboard_event],
                Record.ABBR['input_language']: lang
            }
            self._write(data)
        pass

    # 记录鼠标操作
    def _record_ms_behavior (self, event, loc, stamp):
        if Record.work == True:
            data = {
                Record.ABBR['type']: Record.ABBR['mouse'],
                Record.ABBR['loc']: loc,
                Record.ABBR['time']: skin_time(stamp),
                Record.ABBR['mouse_event']: event
            }
            self._write(data)
        pass

    def _write (self, val):
        str = json.dumps(val)
        r_file = open(Record.ASSETS_DIR + '/index.log', 'a+')
        r_file.write(str + '\n')
        r_file.close()

    def _screen_shot (self, loc, stamp):
        if config.MATCH and Record.work == True:
            screen = Record.scissors.cutScreen()
            Record.scissors.cutUniqueReact(screen, loc, skin_time(stamp))

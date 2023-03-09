import json
import time
import threading
from core.mouse import MouseController
from core.keyboard import KeyboardController
from config import config
from core.controller import createController
from state.handler import Handler as StateHandler
from util.keyboard import get_key_char
from util.scissors import Scissors
from util.times import skin_time
from modules.initbuspace import initbuspace
    
ABBR = config.ABBR
ASSETS_DIR = config.PROJECT['path'] + config.PROJECT['name']
INPUT_SYSTEM = 'ms' # 当前输入法，一般就是讯飞，搜狗，微软，五笔

class Record ():
    # 不传入UI，就说明当前程序用指令运行
    def __init__ (self):
        self.init()
        pass

    def init (self):
        self.ui = None
        self.is_working = False
        self.scissors = Scissors()
        self.state = StateHandler()
        self.m_controller = MouseController()
        self.k_controller = KeyboardController()
        pass

    def _keyboardEvent (self):
        ctrl = createController(Record)()
        self.k_controller.registe({
          'text': self._event_kb_text,
          'press': self._event_kb_press,
          'release': self._event_kb_release,
        })
        self.k_controller.bindExecution(ctrl.execution)
        self.k_controller.active()

    def _createThread (self, event):
        thread = threading.Thread(target=event)
        thread.start()

    def _mouseEvent (self):
        self.m_controller.registe({
          'drop': self._event_ms_drop,
          'move': self._event_ms_move,
          'press': self._event_ms_press,
          'scroll': self._event_ms_scroll,
          'release': self._event_ms_release
        })
        self.m_controller.active()

    def _event_ms_drop (self, event_info):
        self._record_ms_behavior('drop', event_info)
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
        self.is_working = True
        pass

    # 挂载监听事件
    def mount (self):
        self._createThread(self._keyboardEvent)
        self._createThread(self._mouseEvent)

    def stop (self):
        self.k_controller.stop()
        self.m_controller.stop()

    # 记录键盘操作
    # event_info: 'key', 'time_stamp', 'sys_language'
    def _record_kb_behavior (self, keyboard_event, event_info):
        key = event_info['key']
        if keyboard_event != 'text':
            key = get_key_char(key)
        if self.is_working == True:
            data = {
                ABBR['step']: self.state.update_step(),
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
        if self.is_working == True:
            data = {
                ABBR['step']: self.state.update_step(),
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
        if config.MATCH and self.is_working == True:
            screen = self.scissors.cutScreen()
            self.scissors.cutUniqueReact(screen, event_info['loc'], event_info['time_stamp'])

import json
import time
from pynput import keyboard
from config import config
from util.keychar import getKeyChar, isFunctionKey
from util.times import cute_head
import threading

assets_dir = config.PROJECT['path'] + config.PROJECT['name']
abbr = config.ABBR

def standard_key():

  pass

# 辅助键
def is_assist_key(key):
    res = False
    asst_key_chars = [
        'shift','shift_r','alt_l','alt_gr','ctrl_l', 'ctrl_r'
    ]
    asst_keys = [
        keyboard.Key.shift, # 左侧shift
        keyboard.Key.shift_r, # 右侧shift
        keyboard.Key.alt_l, # 左侧alt
        keyboard.Key.alt_gr, # 右侧alt
        keyboard.Key.ctrl_l, # 左侧ctrl
        keyboard.Key.ctrl_r # 右侧ctrl
    ]
    if type(key) == keyboard.Key and key in asst_keys:
        res = True
    if type(key) == str and key in asst_key_chars:
        res = True

    return res

class KeyboardController():
    state = False
    def __init__(self):
        self.combo_keys = []
        self.thread_queue = []
        self.thread_active = None
    def _press(self, key):
        # 如果是辅助键，就存comb，理论上不限定组合键的个数
        if is_assist_key(key) or len(self.combo_keys) > 0:
            if key not in self.combo_keys:
                self._storeCombo(key)
        # try:
        #     print('alphanumeric key {0} pressed'.format(key.char))
        # except AttributeError:
        #     print('special key {0} pressed'.format(key))

    def _release(self, key):
        if is_assist_key(key):
            self._clearCombo() # 如果辅助键松开，那么代表用户取消这次组合键
        else:
            # 有组合键
            if len(self.combo_keys) > 0:
                # 如果配置有功能键，那么就直接触发绑定的事件
                if isFunctionKey(self.combo_keys):
                    self._triggerEvent(self.combo_keys)
                else:
                    self._recordBehavior(self.combo_keys)
            else:
                # 如果配置有功能键，那么就直接触发绑定的事件
                if isFunctionKey(key):
                    self._triggerEvent(key)
                else:
                    self._recordBehavior(key)
        return self._evalExit(key)

    def _evalExit(self, key):
        if self._getState() == False:
            return False
        else:
            return True

    def _storeCombo(self, key):
        if key not in self.combo_keys:
            self.combo_keys.append(key)
        pass

    def _consumeCombo(self):
        pass

    def _clearCombo(self):
        self.combo_keys.clear()

    def start(self):
        self._doActive()
        listener = keyboard.Listener(on_press = self._press, on_release = self._release)
        listener.start()

    def stop(self):
        self._undoActive()

    def bindExecution(self, excutionFn):
        self.eventsExcution = excutionFn

    def _triggerEvent(self, key):
        if (self.eventsExcution):
            thread = threading.Thread(target=self.eventsExcution, args=(key,))
            thread.start()

    def _createSubThread(self, key):
        self.thread_queue.append(threading.Thread(target=self.eventsExcution, args=(key,)))
        pass

    """
    # 使用线程队列的模式,会使主线程被子线程队列的递归逻辑占满,
    # 跑不完子线程,主线程就无法有其他动作
    # 这导致控制器的其他功能无法使用
    """
    def _consumeThread(self):
        if self.thread_active:
            if self.thread_active.is_alive():
                return self._consumeThread()
            else:
                if len(self.thread_queue):
                    self.thread_active = self.thread_queue.pop(0)
                    self.thread_active.start()
                    self.thread_active.join()
                    return self._consumeThread()
        else:
            if len(self.thread_queue):
                self.thread_active = self.thread_queue.pop(0)
                self.thread_active.start()
                self.thread_active.join()
                return self._consumeThread()
        pass

    def _doActive(self):
        KeyboardController.state = True

    def _undoActive(self):
        KeyboardController.state = False

    def _getState(self):
        return KeyboardController.state

    def _recordBehavior(self, key):
        value = {
            abbr['type']: abbr['keyboard'],
            abbr['time']: cute_head(time.time()),
            abbr['key']: getKeyChar(key)
        }
        self._write(value)

    def _write(self, val):
        str = json.dumps(val)
        record_file = open(assets_dir + '/index.log', 'a+')
        record_file.write(str + '\n')
        record_file.close()

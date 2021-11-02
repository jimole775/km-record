import json
import time
from pynput import keyboard
from config import config
from util.keyboard import is_function_key
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
    active = False

    def __init__(self):
        self.combo_keys = []
        self.thread_queue = []
        self.thread_active = None
        self.event_press = None
        self.event_release = None
    # todo 的comb的存取方式不正确
    def _press(self, key):
        # 如果是辅助键，就存comb，理论上不限定组合键的个数123
        if is_assist_key(key) or len(self.combo_keys) > 0:
            if key not in self.combo_keys:
                self._storeCombo(key)
        # try:
        #     print('alphanumeric key {0} pressed'.format(key.char))
        # except AttributeError:
        #     print('special key {0} pressed'.format(key))

    def _release(self, key):
        stamp = time.time()
        # 有组合键
        if len(self.combo_keys) > 0:
            # 如果配置有功能键，那么就直接触发绑定的事件
            if is_function_key(self.combo_keys):
                self._triggerFunction(self.combo_keys)
            else:
                if callable(self.event_release):
                    self.event_release(self.combo_keys, stamp)
            self._clearCombo()
        else:
            # 如果配置有功能键，那么就直接触发绑定的事件
            if is_function_key(key):
                self._triggerFunction(key)
            else:
                if callable(self.event_release):
                    self.event_release(key, stamp)
        return self._evalExit(key)

    def _evalExit(self, key):
        if KeyboardController.active == False:
            return False
        else:
            return True

    def _storeCombo(self, key):
        if key not in self.combo_keys:
            self.combo_keys.append(key)
        pass

    # todo 启用这个方法来进行 “取” comb 操作 
    def _consumeCombo(self, key):
        temp = []
        for item in self.combo_keys:
            if (item != key): temp.append(item)
        self.combo_keys = temp
        pass
        def log():
            print('产生')
            pass
    def _clearCombo(self):
        self.combo_keys.clear()

    def active(self):
        self._doActive()
        with keyboard.Listener(
          on_press=self._press,
          on_release=self._release
        ) as listener:
            listener.join()

    def stop(self):
        self._unActive()

    def bindExecution(self, excutionFn):
        self.eventsExcution = excutionFn

    def _triggerFunction(self, key):
        if (self.eventsExcution):
            thread = threading.Thread(target=self.eventsExcution, args=(key,))
            thread.start()

    def _createSubThread(self, key):
        self.thread_queue.append(threading.Thread(target=self.eventsExcution, args=(key,)))
        pass

    # 注册键盘事件
    def registe(self, event_dict):
        self.event_press = event_dict['press']
        self.event_release = event_dict['release']
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
        KeyboardController.active = True

    def _unActive(self):
        KeyboardController.active = False




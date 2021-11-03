import json
import time
import threading
from pynput import keyboard
from config import config
from util.keyboard import is_function_key, get_key_char
from util.sys import get_sys_language
from util.func import apply
from util.times import skin_time

# 估算系统的中英状态
# 不使用 get_sys_language 的原因是：
#   截图是即时的，切换语法是有延迟的
# 所以，只能在初始的时候使用一次
# 往后只能通过键盘 shift 被按压的次数来判断
def _eval_sys_lang (KC):
    if (KC.sys_language == 'en'):
        KC.sys_language = 'cn'
    elif (KC.sys_language == 'cn'):
        KC.sys_language = 'en'
    else:
        KC.sys_language = 'en'

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
    RANDOM_TYPE_KEY = config.CMD['random_type']['key']
    LANG_TRANS_KEY = 'shift' # 中英切换的键
    sys_language = get_sys_language() # 当前中英文

    def __init__ (self):
        self.combo_info = {
            'keys': [],
            'status': 0 # 0: 闲置中（清空状态）
                        # 1: 按键组合中（shift|ctrl|alt已按下，正在加按其他键）
                        # 97: 未触发功能键，可记录
                        # 98: 已触发功能键，清除中，不可记录
                        # 99: 已触发功能键，可调用功能函数，不可记录
        }
        self.press_keys = []
        self.thread_queue = []
        self.thread_active = None
        self.event_dict = {}
        self.events_excution = None

    # todo 的comb的存取方式不正确
    def _press (self, key):
        stamp = time.time()
        comb_keys = self._get_combo_keys()
        # 如果是辅助键，就存comb，理论上不限定组合键的个数123
        self._store_press(key, stamp)
        if is_assist_key(key) or len(comb_keys) > 0:
            if key not in comb_keys:
                self._store_combo_keys(key)
                comb_keys = self._get_combo_keys()
                # 如果配置有功能键，那么就直接触发绑定的事件
                if is_function_key(comb_keys):
                    # self._trigger_function(comb_keys)
                    self._set_combo_status(99)
        # try:
        #     print('alphanumeric key {0} pressed'.format(key.char))
        # except AttributeError:
        #     print('special key {0} pressed'.format(key))

    def _release (self, key):
        stamp = time.time()
        comb_keys = self._get_combo_keys()
        # 有组合键
        if len(comb_keys) > 0:
            if is_function_key(comb_keys):
                self._trigger_function(comb_keys)

            elif get_key_char(comb_keys) == KeyboardController.RANDOM_TYPE_KEY:
                words = skin_time(time.time())
                self._call_event('text', [words, stamp])

            # 单独点击 shift ctrl alt
            elif len(comb_keys) == 1 and self.combo_info['status'] == 1:
                key_char = get_key_char(key)
                if KeyboardController.LANG_TRANS_KEY == key_char:
                    _eval_sys_lang(KeyboardController)

                self._call_event('release', [key, stamp])

            elif self.combo_info['status'] == 2:
                pass
            # else:
            #     self._call_event('release', [key, stamp])
            self._consume_combo_keys(key)
        else:
            # 如果配置有功能键，那么就直接触发绑定的事件
            if is_function_key(key):
                self._trigger_function(key)
            else:
                self._call_event('release', [key, stamp])
        self._consume_press(key)
        return self._eval_exit()

    def _eval_exit (self):
        if KeyboardController.active == False:
            return False
        else:
            return True

    def _get_combo_keys (self):
        return self.combo_info['keys']

    def _store_combo_keys (self, key):
        if key not in self.combo_info['keys']:
            self.combo_info['keys'].append(key)
            self.combo_info['status'] = 1
        pass

    def _clear_combo_keys (self):
        self.combo_info['keys'].clear()
        self.combo_info['status'] = 0

    def _consume_combo_keys (self, key):
        temp = []
        for item in self.combo_info['keys']:
            if (item != key): temp.append(item)
        self.combo_info['keys'] = temp
        self.combo_info['status'] = 2
        if len(self.combo_info['keys']) == 0:
            self.combo_info['status'] = 0
        pass

    def _store_press (self, key, stamp):
        if key not in self.press_keys:
            self.press_keys.append(key)
            self._call_event('press', [key, stamp])
            # if callable(self.event_press):
            #     self.event_press(key, KeyboardController.sys_language, stamp)
        pass

    def _consume_press (self, key):
        temp = []
        for item in self.press_keys:
            if (item != key): temp.append(item)
        self.press_keys = temp
        pass

    def active (self):
        self._doActive()
        with keyboard.Listener(
          on_press=self._press,
          on_release=self._release
        ) as listener:
            listener.join()

    def stop (self):
        self._unActive()

    def bindExecution (self, excutionFn):
        self.events_excution = excutionFn

    def _trigger_function (self, key):
        if (self.events_excution):
            thread = threading.Thread(target=self.events_excution, args=(key,))
            thread.start()

    def _create_sub_thread (self, key):
        self.thread_queue.append(threading.Thread(target=self.events_excution, args=(key,)))
        pass

    # 注册键盘事件
    def registe (self, event_dict):
        self.event_dict = event_dict
        pass

    def _call_event (self, event_name, params):
        try:
            if type(params) != list: params = [params]
            params.append(KeyboardController.sys_language)
            event_fn = self.event_dict[event_name]
            # 默认往参数的最后一位存储当前系统的输入法标识
            if callable(event_fn):
                apply(event_fn, params)
        except Exception:
            print('is not find methods')
            def log():
                print('中文输入法支持')

    """
    # 使用线程队列的模式,会使主线程被子线程队列的递归逻辑占满,
    # 跑不完子线程,主线程就无法有其他动作
    # 这导致控制器的其他功能无法使用
    """
    def _consume_thread (self):
        if self.thread_active:
            if self.thread_active.is_alive():
                return self._consume_thread()
            else:
                if len(self.thread_queue):
                    self.thread_active = self.thread_queue.pop(0)
                    self.thread_active.start()
                    self.thread_active.join()
                    return self._consume_thread()
        else:
            if len(self.thread_queue):
                self.thread_active = self.thread_queue.pop(0)
                self.thread_active.start()
                self.thread_active.join()
                return self._consume_thread()
        pass

    def _doActive (self):
        KeyboardController.active = True

    def _unActive (self):
        KeyboardController.active = False

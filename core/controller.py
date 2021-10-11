# import pyautogui as gui
# from pynput import keyboard
from config import config
from util.keyboard import get_key_char, compare_keys
# from util.swapdict import swapdict

def createController (_cls): # 继承后，cls原本的变更无法跟踪，需要修改方案
    class HotKeyCtrl(_cls):
        def __init__(self):
            super().__init__()
            pass

        def execution(self, hot_key):
            fn_type = _cls.__name__.lower() # _cls主要是 Record 和 Play 两个类
            p_hot_key = get_key_char(hot_key)
            fn_inst = self._getFnInst(self, fn_type, p_hot_key)
            if callable(fn_inst):
                fn_inst()

        # 获取执行事件实体
        def _getFnInst(self, instance, type, hot_key):
            key_map = config.HOTKEY[type]
            fn_name = self._getFnName(key_map, hot_key)
            if fn_name in dir(instance):
                return eval('instance.' + fn_name)

        # 获取执行事件名字
        def _getFnName(self, key_map, hot_key):
            fn_name = None
            print('hot_key:', hot_key)
            for key_item_name in key_map:
                key_info = key_map[key_item_name]
                if compare_keys(hot_key, key_info['key']) == True:
                    fn_name = key_item_name
                    break
            print('function name:', fn_name)
            return fn_name

    return HotKeyCtrl

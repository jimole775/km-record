# import pyautogui as gui
from pynput import keyboard
from config import config
from util.keychar import get_key_char
# from util.swapdict import swapdict
# key_dicts = {
#     keyboard.Key.f1: 'F1',
#     keyboard.Key.f2: 'F2',
#     keyboard.Key.f3: 'F3',
#     keyboard.Key.f4: 'F4',
#     keyboard.Key.f5: 'F5',
#     keyboard.Key.f5: 'F5',
#     keyboard.Key.f6: 'F6',
#     keyboard.Key.f7: 'F7',
#     keyboard.Key.f8: 'F8',
#     keyboard.Key.f9: 'F9',
#     keyboard.Key.f10: 'F10',
#     keyboard.Key.f11: 'F11',
#     keyboard.Key.f12: 'F12',
# }

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
            for key_item in key_map:
                key_info = key_map[key_item]
                if '+' in hot_key:
                    key_char_list = hot_key.split('+')
                    key_char_list.sort()
                    fn_info_list = key_info['key'].split('+')
                    fn_info_list.sort()
                    if key_char_list == fn_info_list:
                        fn_name = key_item
                elif key_info['key'] == hot_key:
                    fn_name = key_item
            print('function name:', fn_name)
            return fn_name

    return HotKeyCtrl

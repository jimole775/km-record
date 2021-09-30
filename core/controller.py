# import pyautogui as gui
from pynput import keyboard
from config import config
# from util.swapdict import swapdict
key_dicts = {
    keyboard.Key.f1: 'F1',
    keyboard.Key.f2: 'F2',
    keyboard.Key.f3: 'F3',
    keyboard.Key.f4: 'F4',
    keyboard.Key.f5: 'F5',
    keyboard.Key.f5: 'F5',
    keyboard.Key.f6: 'F6',
    keyboard.Key.f7: 'F7',
    keyboard.Key.f8: 'F8',
    keyboard.Key.f9: 'F9',
    keyboard.Key.f10: 'F10',
    keyboard.Key.f11: 'F11',
    keyboard.Key.f12: 'F12',
}
# fn_dicts = {
#     u'开始': 'start',
#     u'结束': 'stop',
#     u'暂停': 'pause',
#     u'循环': 'repeat',
#     u'继续': 'continues',
# }
# class UICtrl(Play):
#     def __init__(self):
#         super().__init__()
#         pass

#     def mount(self, key):
#         event_list = {
#             'F1': self.start,
#             'F2': self.stop
#         }
#         event_list.get(key)()

def createController (_cls): # 继承后，cls原本的变更无法跟踪，需要修改方案
    class HotKeyCtrl(_cls):
        def __init__(self):
            super().__init__()
            pass

        def execution(self, hot_key):
            fn_type = _cls.__name__.lower() # _cls主要是 Record 和 Play 两个类
            fn_inst = self._getFnInst(self, fn_type, hot_key)
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
            for key_item in key_map:
                item = key_map[key_item]
                if hot_key in key_dicts and item['key'] == key_dicts[hot_key]:
                    fn_name = key_item
                    break
            return fn_name

    return HotKeyCtrl

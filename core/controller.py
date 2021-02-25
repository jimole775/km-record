import pyautogui as gui
from pynput import keyboard
from config import config
from util.swapdict import swapdict
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
fn_dicts = {
    u'开始': 'start',
    u'结束': 'stop',
    u'暂停': 'pause',
    u'循环': 'repeat',
    u'继续': 'continues',
}
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

def createController (_cls):
    class HotKeyCtrl(_cls):
        def __init__(self):
            super().__init__()
            pass

        def excution(self, key):
            fn_type = _cls.__name__.lower()
            fn_n = self.getFunction(self, fn_type, key)
            if callable(fn_n):
                fn_n()

        def getFunction(self, instance, type, key):
            hotkey = swapdict(config.HOTKEY[type])
            fn_c = hotkey[key_dicts[key]]
            fn_n = fn_dicts[fn_c]
            if fn_n in dir(instance):
                return eval('instance.' + fn_n)

    return HotKeyCtrl

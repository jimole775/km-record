import time
from pynput import mouse
from util.func import call
from util.times import skin_time

class MouseController:
    def __init__(self):
        self.is_active = False
        self.is_pressed = False
        self.listener = False
        self.event_dict = {}
        self.sx = None
        self.sy = None
        self.x = None
        self.y = None

    def manual_event (self, event_name, *params):
        fn_alias = {
            'press': self._press,
            'release': self._release,
            'move': self._move,
            'scroll': self._scroll
        }
        fn = fn_alias[event_name]
        if callable(fn):
            fn(*params)
        else:
            print(event_name + ' is not support called by manual! => mouse.manual_event')
        pass

    # 监听鼠标滑动
    def _move(self, x, y):
        if self.is_pressed is True:
            self.x = x
            self.y = y
            self._call_event('move', (x, y))
        # 返回 False，监听事件就会注销
        return self.is_active

    # 监听鼠标点击
    def _click(self, x, y, button, pressed):
        self.is_pressed = pressed
        if pressed is True:
            self._press(x, y)
        else:
            self._release(x, y)
        # 返回 False，监听事件就会注销
        return self.is_active

    # 监听鼠标滚轮
    def _scroll(self, x, y, dx, dy):
        self._call_event('scroll', (x, y, dx, dy))
        # 返回 False，监听事件就会注销
        return self.is_active

    def _press(self, x, y):
        self.is_pressed = True
        self.x = self.sx = x
        self.y = self.sy = y
        self._call_event('press', (x, y))
        pass

    def _release(self, x, y):
        self.is_pressed = False
        if (self.x != self.sx or self.y != self.sy):
            self._call_event('drop', (x, y))
        else:
            self._call_event('release', (x, y))
        self.reset()
        pass

    # 注册鼠标事件
    def registe(self, event_dict):
        self.event_dict = event_dict
        pass

    def _call_event (self, event_name, loc):
        try:
            params = {
                'loc': loc,
                'time_stamp': skin_time(time.time())
            }
            event_fn = self.event_dict[event_name]
            if callable(event_fn):
                call(event_fn, params)
        except Exception:
            print('is not register "{}" methods yet in mouse.py'.format(event_name))

    # 开启鼠标监听
    def active(self):
        # 如果 active 还在激活状态，就不再开启 join()
        if self.is_active is True:
            return False
        self._doActive()
        with mouse.Listener(
          on_move=self._move,
          on_click=self._click,
          on_scroll=self._scroll
        ) as listener:
            listener.join()

    # 重置坐标记录，用于判断是否是拖拽行为
    def reset(self):
        self.x = None
        self.y = None
        self.sx = None
        self.sy = None
        pass

    # 关闭监听
    def stop(self):
        self._unActive()
        # self._unWork()

    # 开启监听的逻辑
    def _doActive(self):
        self.is_active = True

    # 关闭监听的逻辑
    def _unActive(self):
        self.is_active = False

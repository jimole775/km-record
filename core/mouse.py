import time
from pynput import mouse
from util.func import call
from util.times import skin_time

class MouseController:
    is_active = False
    def __init__(self):
        self.event_dict = {}
        self.is_pressed = False
        self.listener = False
        self.sx = None
        self.sy = None
        self.x = None
        self.y = None

    # 评估是否退出监听
    def _evalExit(self):
        if MouseController.is_active == False:
            return False
        else:
            return True

    # 监听鼠标滑动
    def _move(self, x, y):
        if self.is_pressed:
            self.x = x
            self.y = y
            self._call_event('move', (x, y))
        return self._evalExit()

    # 监听鼠标点击
    def _click(self, x, y, button, pressed):
        self.is_pressed = pressed
        if self.is_pressed:
            self._press(x, y)
        if not self.is_pressed:
            self._release(x, y)
        return self._evalExit()

    # 监听鼠标滚轮
    def _scroll(self, x, y, dx, dy):
        self._call_event('scroll', (x, y, dx, dy))
        return self._evalExit()

    def _press(self, x, y):
        self.x = self.sx = x
        self.y = self.sy = y
        self._call_event('press', (x, y))

    def _release(self, x, y):
        if (self.x != self.sx or self.y != self.sy):
            self._call_event('drag', (x, y))
        else:
            self._call_event('release', (x, y))
        self.reset()

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
        MouseController.is_active = True

    # 关闭监听的逻辑
    def _unActive(self):
        MouseController.is_active = False

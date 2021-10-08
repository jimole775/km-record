import time
import json
from pynput import mouse
from config import config

assets_dir = config.PROJECT['path'] + config.PROJECT['name']
abbr = config.ABBR

class MouseController:
    # work = False
    active = False
    # behaviors = [
        # { 'event': 'press', 'button': 'left', 'time': '', 'loc': (),  },
        # { 'event': 'move', 'button': 'left', 'time': '', 'loc': () },
        # { 'event': 'release', 'button': 'left', 'time': '', 'loc': () },
        # { 'event': 'scroll', 'button': 'left', 'time': '', 'loc': () }
    # ]
    def __init__(self):
        self.event_drag = None
        self.event_drag_move = None
        self.event_press = None
        self.event_scroll = None
        self.event_release = None
        self.is_pressed = False
        self.listener = False
        self.sx = None
        self.sy = None
        self.x = None
        self.y = None

    # 评估是否退出监听
    def _evalExit(self):
        if MouseController.active == False:
            return False
        else:
            return True

    # 监听鼠标滑动
    def _move(self, x, y):
        timeStamp = time.time()
        if self.is_pressed:
            self.x = x
            self.y = y
            self.event_drag_move((x, y), timeStamp)
            # self._recordBehavior(abbr['drag'], timeStamp, )
        return self._evalExit()

    # 监听鼠标点击
    def _click(self, x, y, button, pressed):
        timeStamp = time.time()
        self.is_pressed = pressed
        print('_click x:', x)
        print('_click y:', y)
        if self.is_pressed:
            # self.event_press((x, y), timeStamp)
            self._press(x, y, timeStamp)
        if not self.is_pressed:
            # self.event_release((x, y), timeStamp)
            self._release(x, y, timeStamp)
        return self._evalExit()

    # 监听鼠标滚轮
    def _scroll(self, x, y, dx, dy):
        timeStamp = time.time()
        self.event_scroll((x, y, dx, dy), timeStamp)
        # self._recordBehavior(abbr['scroll'], timeStamp, (x, y, dx, dy))
        return self._evalExit()

    def _press(self, x, y, timeStamp):
        self.x = self.sx = x
        self.y = self.sy = y
        self.event_press((x, y), timeStamp)

    """
    # todo ctrl + s + a这种是不合理的，不能只判断ctrl有没有release，还要判断s和a有没有release
    """
    def _release(self, x, y, timeStamp):
        if (self.x != self.sx or self.y != self.sy):
            print('trigge drag event')
            self.event_drag((x, y), timeStamp)
        else:
            self.event_release((x, y), timeStamp)
            # self._clickEvent(timeStamp, (x, y))
            # if callable(self.event_click):
            #     self.event_click(x, y, timeStamp)
            # else:
            #     print('没有注册鼠标点击事件！')
        # self._recordBehavior(abbr['release'], timeStamp, (x, y))
        self.reset()

    # 注册鼠标事件
    def registe(self, event_dict):
        self.event_drag = event_dict['drag']
        self.event_drag_move = event_dict['drag_move']
        self.event_press = event_dict['press']
        self.event_scroll = event_dict['scroll']
        self.event_release = event_dict['release']
        pass

    # 开启鼠标监听
    def active(self):
        self._doActive()
        with mouse.Listener(
          on_move=self._move,
          on_click=self._click,
          on_scroll=self._scroll
        ) as listener:
            listener.join()

    # def start(self):
    #     self._doWork()

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

    # def _doWork(self):
    #     MouseController.work = True

    # def _unWork(self):
    #     MouseController.work = False

    # 开启监听的逻辑
    def _doActive(self):
        MouseController.active = True

    # 关闭监听的逻辑
    def _unActive(self):
        MouseController.active = False



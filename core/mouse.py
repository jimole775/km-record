import time
from pynput import mouse
class MouseController:
    state = False
    behaviors = [
        # { 'event': 'press', 'button': 'left', 'time': '', 'loc': (),  },
        # { 'event': 'move', 'button': 'left', 'time': '', 'loc': () },
        # { 'event': 'release', 'button': 'left', 'time': '', 'loc': () },
        # { 'event': 'scroll', 'button': 'left', 'time': '', 'loc': () }
    ]
    def __init__(self, assets_dir):
        self.event_move = None
        self.event_click = None
        self.event_scroll = None
        self.is_pressed = False
        self.listener = False
        self.sx = None
        self.sy = None
        self.x = None
        self.y = None
        self.active = False
        self.assets_dir = assets_dir

    # 评估是否退出监听
    def _evalExit(self):
        if self._getState() == False:
            return False
        else:
            return True

    # 监听鼠标滑动
    def _move(self, x, y):
        timeStamp = time.time()
        if self.is_pressed:
            self.x = x
            self.y = y
            self._recordBehavior('move', timeStamp, (x, y))
        return self._evalExit()

    # 监听鼠标点击
    def _click(self, x, y, button, pressed):
        timeStamp = time.time()
        self.is_pressed = pressed
        self._press(self, x, y, timeStamp)
        self._release(self, x, y, timeStamp)
        return self._evalExit()

    # 监听鼠标滚轮
    def _scroll(self, x, y, dx, dy):
        timeStamp = time.time()
        self._recordBehavior('scroll', timeStamp, (x, y, dx, dy))
        return self._evalExit()

    def _press(self, x, y, timeStamp):
        if self.is_pressed:
            self.x = self.sx = x
            self.y = self.sy = y
            self._recordBehavior('press', timeStamp, (x, y))

    def _release(self, x, y, timeStamp):
        if not self.is_pressed:
            if (self.x != self.sx or self.y != self.sy):
                print('trigge drag event')
            else:
                if callable(self.event_click):
                    self.event_click(x, y, timeStamp)
                else:
                    print('没有注册鼠标点击事件！')
            self.reset()
            self._recordBehavior('release', timeStamp, (x, y))

    # 注册鼠标事件
    def registe (self, event_dict):
        self.event_click = event_dict['click']
        for item in event_dict:
            print(item)
        pass

    # 开启鼠标监听
    def start(self):
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
        self._undoActive()

    # 记录操作
    def _recordBehavior(self, event, time, loc):
        MouseController.behaviors.append({
            'loc': loc,
            'time': time,
            'event': event,
        })
        pass

    # 开启监听的逻辑
    def _doActive(self):
        MouseController.state = True

    # 关闭监听的逻辑
    def _undoActive(self):
        MouseController.state = False

    # 获取监听器的状态
    def _getState(self):
        return MouseController.state

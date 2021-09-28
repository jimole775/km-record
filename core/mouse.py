from pynput import mouse
class MEvent:
    def __init__(self):
        self.clickEvent = None
        self.moveEvent = None
        self.scrollEvent = None
        self.isPressed = False
        self.listener = False
        self.sx = None
        self.sy = None
        self.x = None
        self.y = None
        self.active = False

    def _move(self, x, y):
        if self.isPressed:
            self.x = x
            self.y = y
        # print('move:', x, y)
        # 监听鼠标移动
        # print('Pointer moved to {0}'.format((x, y)))
        pass

    def _click(self, x, y, button, pressed):
        print('click:', button, pressed)
        self.isPressed = pressed
        if self.isPressed:
            self.x = self.sx = x
            self.y = self.sy = y
        if not self.isPressed:
            if (self.x != self.sx or self.y != self.sy):
                print('trigge drag event')
            else:
                print('trigge click event')
                if callable(self.clickEvent):
                    self.clickEvent(x, y, button, pressed)
                else:
                    print('没有注册鼠标点击事件！')
            self._reset()

        # 监听鼠标点击
        # if not pressed:
        #     print('mouse click:', x, y)
        #     screen = self.scissors.cutScreen()
        #     if config.MATCH:
        #         print('MATCH:', config.MATCH)
        #         self.scissors.cutUniqueReact(screen, (x, y))
        #     else:
        #         self.scissors.cutReactAndSave(screen, (x, y))
        # if button == mouse.Button.right:
        #     return False

        # Stop listener
        pass
    def _scroll(self, x, y, dx, dy):
        print('scroll:', dx, dy)
        # 监听鼠标滚轮
        pass

    def registe (self, event_dict):
        self.clickEvent = event_dict['click']
        for item in event_dict:
            print(item)
        # self.moveEvent = event_dict['move']
        # self.scrollEvent = event_dict['scroll']
        pass

    def start(self):
        self.listener = mouse.Listener(
          on_move=self._move,
          on_click=self._click,
          on_scroll=self._scroll
        )
        self.listener.start()
        self._doActive()
        while self.active:
            self.listener.join()

    def _reset(self):
        self.x = None
        self.y = None
        self.sx = None
        self.sy = None
        pass

    def stop(self):
        self._doClose()

    def _doActive(self):
        self.active = True

    def _doClose(self):
        self.active = False

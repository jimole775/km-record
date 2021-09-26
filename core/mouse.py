from pynput import mouse

from util.scissors import Scissors
class MEvent:
    def __init__(self):
        self.scissors = Scissors()
        self.clickEvent = None
        self.moveEvent = None
        self.scrollEvent = None

    def _move(self, x, y):
        # 监听鼠标移动
        # print('Pointer moved to {0}'.format((x, y)))
        pass

    def _click(self, x, y, button, pressed):
        if callable(self.clickEvent):
            self.clickEvent(x, y, button, pressed)
        else:
            print('没有注册鼠标点击事件！')
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
        # 监听鼠标滚轮
        pass

    def registe (self, event_dict):
        
        pass

    def start(self):
        with mouse.Listener(
          on_move=self._move,
          on_click=self._click,
          on_scroll=self._scroll
        ) as mlistener:
            mlistener.join()

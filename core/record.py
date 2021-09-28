from core.mouse import MEvent
from core.keyboard import KEvent
from config import config
from pynput import mouse
from core.controller import createController
from util.scissors import Scissors
import threading
# class Monitor (threading.Thread):
#     def __init__ (self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter

#     def run (self):
#         if self.name == 'Thread-1':
#             kEvent = KEvent()
#             kEvent.start()
#         if self.name == 'Thread-2':
#             mEvent = MEvent()
#             mEvent.start()

class Record ():
    def __init__ (self):
        self.scissors = Scissors()
        self.kEvent = KEvent()
        self.mEvent = MEvent()
        pass

    def _createThread (self, event):
        thread = threading.Thread(target=event)
        thread.start()

    # def run (self):
    #     self.__createThread__(self.__keyboardEvent__)

    # def __createThread__ (self, event):
    #     thread = threading.Thread(target=event)
    #     thread.start()

    # def __keyboardEvent__ (self):
    #     kEvent = KEvent()
    #     ctrl = createController(Play)()
    #     kEvent.bindExecution(ctrl.execution)
    #     kEvent.start()

    def _keyboardEvent (self):
        ctrl = createController(Record)()
        self.kEvent.bindExecution(ctrl.execution)
        self.kEvent.start()

    def _mouseEvent (self):
        self.mEvent.registe({
          'click': self._clickEvent,
          'drag': self._dragEvent
        })
        self.mEvent.start()

    def run (self):
        # 创建新线程
        # monitor1 = Monitor(1, 'Thread-1', 1)
        # monitor2 = Monitor(2, 'Thread-2', 2)
        # monitor1.setDaemon(True) # 主线程关闭, 子线程将被摧毁
        # monitor2.setDaemon(True) # 主线程关闭, 子线程将被摧毁
        # monitor1.start()
        # monitor2.start()
        self._createThread(self._keyboardEvent)
        self._createThread(self._mouseEvent)
        # 轮询线程状态, 如果有一个关闭, 则让主线程关闭
        # while True:
        #     if (monitor1.is_alive() == False or monitor2.is_alive() == False):
        #         break
    def _clickEvent (self, x, y, button, pressed):
        # 监听鼠标点击
        if not pressed:
            screen = self.scissors.cutScreen()
            if config.MATCH:
                print('MATCH:', config.MATCH)
                self.scissors.cutUniqueReact(screen, (x, y))
            else:
                self.scissors.cutReactAndSave(screen, (x, y))
        if button == mouse.Button.right:
            return False

    def _dragEvent (self, x, y, button, pressed):
        print('drag')
        pass

    def stop (self):
        self.kEvent.stop()
        self.mEvent.stop()

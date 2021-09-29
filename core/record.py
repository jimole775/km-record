from core.mouse import MouseController
from core.keyboard import KeyboardController
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
#             k_controller = KeyboardController()
#             k_controller.start()
#         if self.name == 'Thread-2':
#             m_controller = MouseController()
#             m_controller.start()

class Record ():
    def __init__ (self):
        assets_dir = config.PROJECT['path'] + config.PROJECT['name']
        self.scissors = Scissors(assets_dir)
        self.k_controller = KeyboardController(assets_dir)
        self.m_controller = MouseController(assets_dir)
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
    #     k_controller = KeyboardController()
    #     ctrl = createController(Play)()
    #     k_controller.bindExecution(ctrl.execution)
    #     k_controller.start()

    def _keyboardEvent (self):
        ctrl = createController(Record)()
        self.k_controller.bindExecution(ctrl.execution)
        self.k_controller.start()

    def _mouseEvent (self):
        self.m_controller.registe({
          'click': self._clickEvent,
          'drag': self._dragEvent
        })
        self.m_controller.start()

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
    def _clickEvent (self, x, y, stamp):
        screen = self.scissors.cutScreen()
        if config.MATCH:
            print('MATCH:', config.MATCH)
            self.scissors.cutUniqueReact(screen, (x, y), stamp)
        else:
            self.scissors.cutReactAndSave(screen, (x, y), stamp)

    def _dragEvent (self, x, y, button, pressed):
        print('drag')
        pass

    def stop (self):
        self.k_controller.stop()
        self.m_controller.stop()

from pynput import keyboard
from config import config
import threading
def standard_key():
  pass
def is_assist_key(key):
  # pressed会在released之前,需要一致记录并去重
  # shift Key.shift Key.shift_r
  # alt Key.alt_l key.alt_gr
  # ctrl Key.ctrl_l Key.ctrl_r
  asst_keys = [
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_gr,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r
  ]
  return ass_keys.index(key) > -1


class KEvent():
    def __init__ (self):
        self.combo_keys = []
        self.thread_queue = []
        self.thread_active = None
        self.listener = None
        self.active = False

    def on_press (self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release (self, key):
        self.consumeCombo()
        self.clearCombo()
        self.triggerEvent(key)
        print(key)
        if key == keyboard.Key.esc:
            return False

    def storeCombo (self):
        pass

    def consumeCombo (self):
        pass

    def clearCombo (self):
        self.combo_keys = []

    def start (self):
        self.listener = keyboard.Listener(on_press = self.on_press, on_release = self.on_release)
        self.listener.start()
        # self._doActive()
        # while self.active:
        #     self.listener.join()

    def bindExecution (self, excutionFn):
        self.eventsExcution = excutionFn

    def triggerEvent (self, key):
        if (self.eventsExcution):
            thread = threading.Thread(target=self.eventsExcution, args=(key,))
            thread.start()

    def createSubThrd (self, key):
        self.thread_queue.append(threading.Thread(target=self.eventsExcution, args=(key,)))
        pass


    """
    # 使用线程队列的模式,会使主线程被子线程队列的递归逻辑占满,
    # 跑不完子线程,主线程就无法有其他动作
    # 这导致控制器的其他功能无法使用
    """
    def consumeThrd (self):
        if self.thread_active:
            if self.thread_active.is_alive():
                return self.consumeThrd()
            else:
                if len(self.thread_queue):
                    self.thread_active = self.thread_queue.pop(0)
                    self.thread_active.start()
                    self.thread_active.join()
                    return self.consumeThrd()
        else:
            if len(self.thread_queue):
                self.thread_active = self.thread_queue.pop(0)
                self.thread_active.start()
                self.thread_active.join()
                return self.consumeThrd()
        pass

    def stop(self):
        self.listener.stop()

    def restart(self):
        self.listener.start()

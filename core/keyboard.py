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
  return asst_keys.index(key) > -1

class KeyboardController():
    state = False
    def __init__ (self, assets_dir):
        self.combo_keys = []
        self.thread_queue = []
        self.thread_active = None
        self.r_file = open(assets_dir + '/index.json', 'w')

    def _press (self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def _release (self, key):
        self._clearCombo()
        self._triggerEvent(key)
        self.r_file.write(123)
        return self._evalExit(key)

    def _evalExit(self, key):
        if key == keyboard.Key.esc or self._getState() == False:
            return False
        else:
            return True

    def _storeCombo (self):
        pass

    def _consumeCombo (self):
        pass

    def _clearCombo (self):
        self.combo_keys = []

    def start (self):
        self._doActive()
        listener = keyboard.Listener(on_press = self._press, on_release = self._release)
        listener.start()

    def stop(self):
        self._undoActive()

    def bindExecution (self, excutionFn):
        self.eventsExcution = excutionFn

    def _triggerEvent (self, key):
        if (self.eventsExcution):
            thread = threading.Thread(target=self.eventsExcution, args=(key,))
            thread.start()

    def _createSubThread (self, key):
        self.thread_queue.append(threading.Thread(target=self.eventsExcution, args=(key,)))
        pass

    """
    # 使用线程队列的模式,会使主线程被子线程队列的递归逻辑占满,
    # 跑不完子线程,主线程就无法有其他动作
    # 这导致控制器的其他功能无法使用
    """
    def _consumeThread (self):
        if self.thread_active:
            if self.thread_active.is_alive():
                return self._consumeThread()
            else:
                if len(self.thread_queue):
                    self.thread_active = self.thread_queue.pop(0)
                    self.thread_active.start()
                    self.thread_active.join()
                    return self._consumeThread()
        else:
            if len(self.thread_queue):
                self.thread_active = self.thread_queue.pop(0)
                self.thread_active.start()
                self.thread_active.join()
                return self._consumeThread()
        pass

    def _doActive(self):
        KeyboardController.state = True

    def _undoActive(self):
        KeyboardController.state = False

    def _getState(self):
        return KeyboardController.state

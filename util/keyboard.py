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
  ass_keys = [
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_gr,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r
  ]
  return ass_keys.index(key) > -1
class KEvent:
  def __init__(self):
    self.hook = None
    self.combo_keys = []
    self.assets_path = config.ASSETS_PATH
    self.object_name = config.OBJECT_NAME

  def on_press(self, key):
    try:
      print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
      print('special key {0} pressed'.format(key))

  def on_release(self, key):
    self.consumeCombo()
    self.clearCombo()
    self.triggerHooker(key)
    if key == keyboard.Key.esc:
      return False

  def store_combo(self):
    pass

  def consumeCombo(self):
    pass

  def clearCombo(self):
    self.combo_keys = []

  def start(self, hook = None):
    self.hook = hook
    with keyboard.Listener(on_press = self.on_press, on_release = self.on_release) as klistener:
      klistener.join()

  def triggerHooker(self, key):
    if (self.hook):
      thread = self.crtSubThrd(key)
      thread.start()

  def crtSubThrd(self, key):
      return threading.Thread(target=self.hook, args=(key,))

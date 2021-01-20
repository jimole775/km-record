from pynput import keyboard
from config import config
def standard_key():
  pass
def assist_key():
  # pressed会在released之前,需要一致记录并去重
  # shift Key.shift Key.shift_r
  # alt Key.alt_l key.alt_gr
  # ctrl Key.ctrl_l Key.ctrl_r
  pass
class KEvent:
  def __init__(self):
    self.assets_path = config.ASSETS_PATH
    self.object_name = config.OBJECT_NAME
  def on_press(self, key):
    try:
      print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
      print('special key {0} pressed'.format(key))

  def on_release(self, key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
      return False

  def start(self):
    with keyboard.Listener(on_press = self.on_press, on_release = self.on_release) as klistener:
      klistener.join()

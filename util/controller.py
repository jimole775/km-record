import pyautogui as gui
import numpy as np
import os
import re
import time
from util.play import Play
from pynput import keyboard
class UICtrl(Play):
  def __init__(self):
    super().__init__()
    pass

  def mount(self, key):
    event_list = {
      'F1': self.start,
      'F2': self.stop
    }
    event_list.get(key)()

class HotKeyCtrl(Play):
  def __init__(self):
    super().__init__()
    pass

  def mount(self, key):
    event_list = {
      keyboard.Key.f1: self.start,
      keyboard.Key.f2: self.repeat,
      keyboard.Key.f3: self._pause,
      keyboard.Key.f4: self._continue,
      keyboard.Key.f5: self.stop,
    }
    fn = event_list.get(key)
    if fn:
      if callable(fn):
        fn()

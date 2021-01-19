from pynput import mouse
from util.scissor import Scissor
scissor = Scissor()
class MEvent:
  def __init__(self, object_name):
    self.object_name = object_name
  def on_move(self, x, y):
    # 监听鼠标移动
    # print('Pointer moved to {0}'.format((x, y)))
    pass

  def on_click(self, x, y, button, pressed):
    # 监听鼠标点击
    print(x, y, button, pressed)
    if not pressed:
      scissor.cutReact((x, y)).save(self.object_name)
      # Stop listener
      # return False

  def on_scroll(self, x, y, dx, dy):
    # 监听鼠标滚轮
    pass

  def start(self):
    with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as mlistener:
      mlistener.join()

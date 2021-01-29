from pynput import mouse
from config import config
from util.scissors import Scissors
class MEvent:
  def __init__(self):
    self.scissors = Scissors()
  def on_move(self, x, y):
    # 监听鼠标移动
    # print('Pointer moved to {0}'.format((x, y)))
    pass

  def on_click(self, x, y, button, pressed):
    # 监听鼠标点击
    if not pressed:
      print('mouse click:', x, y)
      screen = self.scissors.cutScreen()
      if config.MATCH:
        self.scissors.cutUniqueReact(screen, (x, y))
      else:
        self.scissors.cutReactAndSave(screen, (x, y))
    if button == mouse.Button.right:
      return False
    # Stop listener

  def on_scroll(self, x, y, dx, dy):
    # 监听鼠标滚轮
    pass

  def start(self):
    with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as mlistener:
      mlistener.join()

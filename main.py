from util.mouse import MEvent
from util.keyboard import KEvent
from util.mkdir import mkdir
import threading
import sys
object_name = sys.argv[1]
mkdir( '.\\objects\\' + object_name)
class myThread (threading.Thread):
  def __init__(self, threadID, name, counter):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.counter = counter
  def run(self):
    if (self.name == 'Thread-1'):
      kEvent = KEvent(object_name)
      kEvent.start()
    # if (self.name == 'Thread-2'):
    #   mEvent = MEvent(object_name)
    #   mEvent.start()
# 创建新线程
thread1 = myThread(1, 'Thread-1', 1)
thread2 = myThread(2, 'Thread-2', 2)
thread1.start()
thread2.start()

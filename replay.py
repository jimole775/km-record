from core.keyboard import KEvent
from core.controller import HotKeyCtrl
# play = Play()
keyCtrl = HotKeyCtrl()
keyCtrl.getSteps()
kEvent = KEvent(keyCtrl.mount)
kEvent.start()
# while True:
# keyCtrl.start()
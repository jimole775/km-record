from util.keyboard import KEvent
from util.controller import HotKeyCtrl
from config import config
# play = Play()
keyCtrl = HotKeyCtrl()
keyCtrl.getSteps(config.ASSETS_PATH + config.OBJECT_NAME)
kEvent = KEvent(keyCtrl.mount)
kEvent.start()
# while True:
# keyCtrl.start()
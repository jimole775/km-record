from util.keyboard import KEvent
from util.controller import KeyCtrl
from config import config
# play = Play()
kEvent = KEvent()
keyCtrl = KeyCtrl()
keyCtrl.getSteps(config.ASSETS_PATH + config.OBJECT_NAME)
kEvent.start(keyCtrl.mount)
# while True:
# keyCtrl.start()
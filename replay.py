from util.play import Play
from config import config
play = Play()
play.getSteps(config.ASSETS_PATH + config.OBJECT_NAME)
while True:
  play.run()
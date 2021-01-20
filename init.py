from config import config
from util.mkdir import mkdir
from util.rmdir import rmdir
import os
objectDir = config.ASSETS_PATH + config.OBJECT_NAME
# 如果目录已经存在,先删除之
if os.path.exists(objectDir) == True:
  rmdir(objectDir)
  mkdir(objectDir)
else:
  mkdir(objectDir)
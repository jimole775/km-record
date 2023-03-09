from config import config
from util.mkdir import mkdir
from util.rmdir import rmdir
import os
def initbuspace (pro_name):
    object_dir = config.PROJECT['path'] + (pro_name | config.PROJECT['name'])
    # 如果目录已经存在,先删除之
    if os.path.exists(object_dir) == True:
        rmdir(object_dir)
        mkdir(object_dir)
    else:
        mkdir(object_dir)

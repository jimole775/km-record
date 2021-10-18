from util.scaner import Scaner
from util.scissors import Scissors
from util.monitor import get_task_bar_pos
from config import config


sys_assets_path = config.ASSETS['path'] + '\\sys'

def get_icon(name):
    icons = {
        'win': sys_assets_path + '\\win10\\{}.png'.format(name),
        'en': sys_assets_path + '\\win10\\{}.png'.format(name),
        'en_b': sys_assets_path + '\\win10\\{}.png'.format(name),
        'cn': sys_assets_path + '\\win10\\{}.png'.format(name)
    }
    return icons[name]

def isWin():
  return True

def isMac():
  return False

def isUnx():
  return False

def isEnType():
  return False

def isCnType():
  return False

def get_task_bar():
    scissors = Scissors()
    scaner = Scaner()
    # x1, y1, x2, y2 = get_task_bar_pos()
    task_bar = scissors.cutReact(get_task_bar_pos())
    isEn = scaner.hasUniqueTarget(scaner.toGray(task_bar), get_icon('en_b'))
    print(isEn)
    # # 左侧或者上侧
    # if x1 == y1 == 0:
    #     if (x2 > y2): # 上侧
    #         react = scissors.cutReact((x1, y1, y2, y2))
    #     elif (y2 > x2): # 左侧
    #         react = scissors.cutReact((x1, y1, x2, x2))
    #     print(scaner.hasUniqueTarget(react, get_icon('win')))

    # # 下侧
    # elif x1 == 0 and y1 != 0:
    #     bar_height = y2 - y1
    #     react = scissors.cutReact((x1, y1, bar_height, y2))
    #     print(scaner.hasUniqueTarget(react, get_icon('win')))

    # # 右侧
    # elif x1 != 0 and y1 == 0:
    #     bar_width = y2 - (x2 - x1)
    #     react = scissors.cutReact((x1, y1, x2, bar_width))
    #     print(scaner.hasUniqueTarget(react, get_icon('win')))

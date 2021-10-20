from util.scaner import Scaner
from util.scissors import Scissors
from util.monitor import get_task_bar_pos
from config import config

scaner = Scaner()
scissors = Scissors()

sys_assets_path = config.ASSETS['path'] + '\\sys'

def get_icon(name):
    icons = {
        'win': sys_assets_path + '\\win10\\{}',
        'en': sys_assets_path + '\\win10\\{}',
        'en_sg': sys_assets_path + '\\win10\\{}',
        'cn': sys_assets_path + '\\win10\\{}',
    }
    return icons[name].format(name)

def isWin():
  return True

def isMac():
  return False

def isUnx():
  return False

def isEnType():
    en = _get_gray_negative(get_icon('en.png'))
    en_sg = _get_gray_negative(get_icon('en_sg.png'))
    task_bar = _get_gray_negative(scissors.cutReact(get_task_bar_pos()))
    return scaner.hasUniqueTarget(task_bar, en) or scaner.hasUniqueTarget(task_bar, en_sg)

def isCnType():
    cn = _get_gray_negative(get_icon('cn.png'))
    cn_sg = _get_gray_negative(get_icon('cn_sg.png'))
    task_bar = _get_gray_negative(scissors.cutReact(get_task_bar_pos()))
    return scaner.hasUniqueTarget(task_bar, cn) or scaner.hasUniqueTarget(task_bar, cn_sg)

def _get_gray_negative(img):
    return scaner.toNegative(scaner.toGray(img))


# def get_task_bar():
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

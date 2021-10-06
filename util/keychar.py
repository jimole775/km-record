import re
from config import config
from pynput import keyboard

def getSingleKeyChar(key):
    keyChar = key
    # 普通键位 a b c d e f g ...
    if (type(key) == keyboard._win32.KeyCode):
        keyChar = getattr(key, 'char')

    # 特殊键位包括 辅助键 shift 之类的，还包括 F1 F2 之类的
    if (type(key) == keyboard.Key):
        keyChar = getattr(key, 'name')

    return keyChar

# [keyboard.Key.ctrl_l, keyboard.Key.d] => 'ctrl + d'
def getCombKeyChar(comb_key):
    res = ''
    print('comb_key', comb_key)
    for key in comb_key:
        key_char = getSingleKeyChar(key)
        print('key:', key, ', char:', key_char)
        key_char = flatAsstKey(key_char)
        print('flatAsstKey:', key_char)
        res = res + '+' + key_char
        
    return res[1:]


# 功能键部分左右，所以去掉 'ctrl_l' 的 '_l'，返回 'ctrl'
def flatAsstKey(key):
    signs = ['ctrl', 'alt', 'shift']
    key_char = getSingleKeyChar(key)
    res = None
    for item in signs:
        if (re.match(item, key_char)):
            res = item
            break
    if not res:
        res = key_char
    return res

# 获取 key 的字符串类型
def getKeyChar(key_or_comb):
    key_char = ''
    key_type = type(key_or_comb)
    # 组合键
    if (key_type == list):
        key_char = getCombKeyChar(key_or_comb)
    # 字符串
    elif (key_type == str):
        key_char = key_or_comb
    # 单键
    else:
        key_char = getSingleKeyChar(key_or_comb)
    return key_char

# 判断是否是功能键，包括组合键
def isFunctionKey(key_or_comb):
    res = False
    for fn_type in config.HOTKEY:
        name_map = config.HOTKEY[fn_type]
        for fn_name in name_map:
            fn_info = name_map[fn_name]
            key_char = getKeyChar(key_or_comb)
            if fn_info['key'] == key_char:
                res = True
                break
        if res == True:
            break

    return res

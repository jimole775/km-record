import re
from config import config
from pynput import keyboard

def _get_single_key(_t, key):
    res = key
    # 普通键位 a b c d e f g ...
    if (type(key) == keyboard._win32.KeyCode):
        res = getattr(key, 'vk')
        if _t == 'char':
            res = chr(res).lower()

    # 特殊键位包括 辅助键 shift 之类的，还包括 F1 F2 之类的
    if (type(key) == keyboard.Key):
        if _t == 'char':
            res = getattr(key, 'name')
        if _t == 'code':
            res = getattr(key, 'value')
    return res

# [keyboard.Key.ctrl_l, keyboard.Key.d] => 'ctrl + d'
def _get_comb_key(_t, comb_key):
    res = ''
    for key in comb_key:
        _key = _get_single_key(_t, key)
        if (_t == 'char'):
            _key = flat_asst_key(_key)
        res = res + '+' + _key
    return res[1:] # 去掉首部的 + 号

# 功能键部分左右，所以去掉 'ctrl_l' 的 '_l'，返回 'ctrl'
def flat_asst_key(key):
    signs = ['ctrl', 'alt', 'shift']
    key_char = _get_single_key('char', key)
    res = None
    for item in signs:
        if (re.match(item, key_char)):
            res = item
            break
    if not res:
        res = key_char
    return res

# 获取 key 的字符类型
def get_key_char(key_or_comb):
    res = ''
    key_type = type(key_or_comb)
    # 组合键
    if (key_type == list):
        res = _get_comb_key('char', key_or_comb)
    # 字符串
    elif (key_type == str):
        res = key_or_comb
    # 单键
    else:
        res = _get_single_key('char', key_or_comb)
    return res

# 获取 key 的数字类型
def get_key_code(key_or_comb):
    res = ''
    key_type = type(key_or_comb)
    # 组合键
    if (key_type == list):
        res = _get_comb_key('code', key_or_comb)
    # 统一转成字符串
    elif (key_type == int):
        res = str(key_or_comb)
    # 字符串
    elif (key_type == str):
        res = key_or_comb
    # 单键
    else:
        res = _get_single_key('code', key_or_comb)
    return res

# 判断是否是功能键，包括组合键
def is_function_key(key_or_comb):
    res = False
    for fn_type in config.HOTKEY:
        name_map = config.HOTKEY[fn_type]
        for fn_name in name_map:
            fn_info = name_map[fn_name]
            key_char = get_key_char(key_or_comb)
            if '+' in key_char:
                key_char_list = key_char.split('+')
                key_char_list.sort()
                fn_info_list = fn_info['key'].split('+')
                fn_info_list.sort()
                if key_char_list == fn_info_list:
                    res = True
            elif fn_info['key'] == key_char:
                res = True
                break
        if res == True:
            break
    return res

key_map = {
    'ctrl': keyboard.Key.ctrl,
    'shift': keyboard.Key.shift,
    'alt': keyboard.Key.alt,
    'space': keyboard.Key.space,
    'esc': keyboard.Key.esc,
    'enter': keyboard.Key.enter,
    'page_down': keyboard.Key.page_down,
    'page_up': keyboard.Key.page_up,
    'caps_lock': keyboard.Key.caps_lock,
    'tab': keyboard.Key.tab,
    'backspace': keyboard.Key.backspace,
    'delete': keyboard.Key.delete,
    'insert': keyboard.Key.insert
}

def getKeyObj(str_key):
    if (type(str_key) == str) and (str_key in key_map):
        return key_map[str_key]
    else:
        return str_key
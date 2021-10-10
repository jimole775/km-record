import re
from config import config
from pynput import keyboard
def _eval_single(exp_t, src):
    res = src
    s_type = type(src)
    if exp_t == 'code':
        if s_type == str:
            if (len(src) == 1):
                res = ord(src)
            else:
                key = keyboard.Key[src]
                res = getattr(key, 'value')
        if s_type == keyboard._win32.KeyCode:
            res = getattr(src, 'vk')
        if s_type == keyboard.Key:
            res = getattr(src, 'value')

    if exp_t == 'char':
        if s_type == int:
            key = keyboard.KeyCode.from_vk(src)
            if (type(key) == keyboard.Key):
                res = getattr(key, 'name')
                res = flat_asst_key(res)
            else:
                res = chr(src).lower()
        if s_type == keyboard._win32.KeyCode:
            code = getattr(src, 'vk')
            res = chr(code).lower()
        if s_type == keyboard.Key:
            res = getattr(src, 'name')
            res = flat_asst_key(res)

    if exp_t == 'key':
        if s_type == int:
            res = keyboard.KeyCode.from_vk(src)
        if s_type == str:
            if len(src) == 1:
                code = ord(src)
                res = keyboard.KeyCode.from_vk(code)
            else:
                res = keyboard.Key[src]
    return res

def _eval_comb(exp_t, comb_key_list):
    res = []
    for key in comb_key_list:
        _key = _eval_single(exp_t, key)
        if (exp_t == 'char'):
            _key = flat_asst_key(_key)
        res.append(_key)
    res.sort()
    return res

# 获取 key 的字符类型
def get_key_char(src):
    res = None
    key_type = type(src)
    # 组合键
    if (key_type == list):
        res = _eval_comb('char', src)
    # 字符串
    elif (key_type == str):
        if '+' in src:
            res = _eval_comb('char', src.split('+'))
        else:
            res = _eval_single('char', src)
    # 单键
    else:
        res = _eval_single('char', src)
    return res

# 获取 key 的数字类型
def get_key_code(src):
    res = None
    key_type = type(src)
    # 组合键
    if (key_type == list):
        res = _eval_comb('code', src)
    # 统一转成字符串
    elif (key_type == int):
        res = str(src)
    # 字符串
    elif (key_type == str):
        if '+' in str:
            res = _eval_comb('code', src.split('+'))
        else:
            res = _eval_single('code', src)
    # 单键
    else:
        res = _eval_single('code', src)
    return res

def get_keyboard_key(src):
    res = None
    key_type = type(src)
    # 组合键
    if (key_type == list):
        res = _eval_comb('key', src)
    # 字符串
    elif (key_type == str):
        if '+' in str:
            res = _eval_comb('key', src.split('+'))
        else:
            res = _eval_single('key', src)
    # 单键
    else:
        res = _eval_single('key', src)
    return res

# 功能键部分左右，所以去掉 'ctrl_l' 的 '_l'，返回 'ctrl'
def flat_asst_key(key):
    signs = ['ctrl', 'alt', 'shift']
    key_char = _eval_single('char', key)
    res = key
    for sign in signs:
        if (re.match(sign, key_char)):
            res = sign
            break
    return res

# 判断是否是功能键，包括组合键
def is_function_key(key_or_comb):
    res = False
    # 保证 key_char 转换后的格式
    key_char = get_key_char(key_or_comb)
    if type(key_char) == list:
        key_char.sort()
    for fn_type in config.HOTKEY:
        name_map = config.HOTKEY[fn_type]
        for fn_name in name_map:
            fn_info = name_map[fn_name]
            fn_key_char = get_key_char(fn_info['key'])
            if type(fn_key_char) == list:
                fn_key_char.sort()
            if fn_key_char == key_char:
                res = True
                break
        if res == True:
            break
    return res

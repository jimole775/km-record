import re
from config import config
from pynput import keyboard

RANDOM_TYPE_KEY = config.CMD['random_type']['key']
# 获取 key 的字符类型
def get_key_char(src):
    return _transform_handler('char', src)

# 获取 key 的数字类型
def get_key_code(src):
    # 统一转成字符串
    if (type(src) == int):
        return str(src)
    else:
        return _transform_handler('code', src)

# 获取 key 的对象类型
def get_keyboard_key(src):
    return _transform_handler('key', src)

def is_random_key(key_or_comb):
    keys = get_keyboard_key(key_or_comb)
    if type(keys) != list:
        keys = [keys]
    # 额外增加一个输入随机数的指令
    random_keys = get_keyboard_key(RANDOM_TYPE_KEY)
    return compare_keys(keys, random_keys)

def include_random_key(key_or_comb):
    res = False
    keys = get_keyboard_key(key_or_comb)
    if type(keys) != list:
        keys = [keys]
    # 额外增加一个输入随机数的指令
    random_keys = get_keyboard_key(RANDOM_TYPE_KEY)
    for key in keys:
        if key in random_keys:
            res = True
            break
    return res

def include_function_key(key_or_comb):
    res = False
    keys = get_keyboard_key(key_or_comb)
    if type(keys) != list:
        keys = [keys]
    for fn_type in config.HOTKEY:
        name_map = config.HOTKEY[fn_type]
        for fn_name in name_map:
            fn_info = name_map[fn_name]
            fn_keys = get_keyboard_key(fn_info['key'])
            for key in keys:
                if key in fn_keys:
                    res = True
                    break
            if res == True:
                break
        if res == True:
            break
    return res

# 判断是否是功能键，包括组合键
def is_function_key(key_or_comb):
    res = False
    # 保证 key_char 转换后的格式
    key_char = get_key_char(key_or_comb)
    for fn_type in config.HOTKEY:
        name_map = config.HOTKEY[fn_type]
        for fn_name in name_map:
            fn_info = name_map[fn_name]
            fn_key_char = get_key_char(fn_info['key'])
            if compare_keys(fn_key_char, key_char):
                res = True
                break
        if res == True:
            break

    # 额外增加一个输入随机数的指令
    random_key_char = get_key_char(RANDOM_TYPE_KEY)
    if compare_keys(random_key_char, key_char): res = True
    return res

# 比对两个键的code是否相等，支持不同类型的比对
def compare_keys(l_k, r_k):
    if type(l_k) == type(r_k) or _both_in_combs(l_k, r_k) or _both_in_combs(r_k, l_k):
        l_code = get_key_char(l_k)
        r_code = get_key_char(r_k)
        if type(l_code) == list:
            l_code.sort()
            r_code.sort()
        return l_code == r_code
    else:
        return False

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

def _eval_single(exp_t, src):
    res = src
    s_type = type(src)
    if exp_t == 'code': # 返回 code
        if s_type == str: # char 转 code
            if (len(src) == 1):
                res = ord(src.upper())
            else:
                key = keyboard.Key[src]
                res = getattr(key, 'value')
        if s_type == keyboard._win32.KeyCode:
            res = getattr(src, 'vk')
        if s_type == keyboard.Key:
            res = getattr(src, 'value')

    if exp_t == 'char': # 返回 char
        if s_type == int: # int 转 char
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

    if exp_t == 'key': # 返回 key 对象
        if s_type == int: # int 转 key
            res = keyboard.KeyCode.from_vk(src)
        if s_type == str: # char 转 key
            if len(src) == 1:
                code = ord(src.upper())
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
    return res

def _transform_handler(exp_t, src):
    res = None
    key_type = type(src)
    # 组合键
    if (key_type == list):
        res = _eval_comb(exp_t, src)
    # 字符串
    elif (key_type == str):
        if '+' in src:
            res = _eval_comb(exp_t, src.split('+'))
        else:
            res = _eval_single(exp_t, src)
    # 单键
    else:
        res = _eval_single(exp_t, src)
    return res

def _both_in_combs(l_k, r_k):
    return type(l_k) == list and type(r_k) == str and '+' in r_k

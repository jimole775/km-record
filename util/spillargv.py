from util.asserts import Assert
import re
r_is_params = r'^(.*?):(.+)$'
r_multi_params = r'(.*?);(.+)$'
r_attrs_params = r'(.*?),(.+)$'
r_eval_params = r'(.*?)=(.+)$'
r_has_suffix = r'.+;$'
obj_split_char = ';'
attr_split_char = ','
eval_char = '='

asserts = Assert()
# 校准值的类型
def __correctCatlog__(def_conf, val):
  if asserts.isNumber(val):
    def_conf = val * 1
  if asserts.isBoolean(val):
    def_conf = eval(val)
  else:
    def_conf = val

# 赋值操作
def __evalHandle__(def_conf, param_str):
  if re.search(r_attrs_params, param_str):
    attrs = param_str.split(attr_split_char)
    for attr in attrs:
      _key, _val = attr.split(eval_char)
      __correctCatlog__(def_conf[_key], _val)
  else:
    if re.search(r_eval_params, param_str):
      _key, _val = param_str.split(eval_char)
      __correctCatlog__(def_conf[_key], _val)
    else:
      __correctCatlog__(def_conf, param_str)


"""
# 指令样例：
# py record match:False;
# py record match:times=5,interval=0.5;
# py record hotkey:play:F1=开始,F2=暂停;record:F1=开始;
"""
def __children__(def_conf, parent_val):
  obj_arr = parent_val.split(obj_split_char)
  for obj in obj_arr:
    c_param = re.search(r_is_params, obj, re.I)
    if c_param:
      c_param_key = c_param[1]
      c_param_val = c_param[2]
      def_conf[c_param_key] = {}
      nextlvl = re.search(r_multi_params, c_param_val, re.I)
      if nextlvl:
        __children__(def_conf[c_param_key], c_param_val)
      else:
        __evalHandle__(def_conf[c_param_key], c_param_val)

def cutSuffix(val):
  if re.search(r_has_suffix, val, re.I):
    return val[:len(val) - 1]
  else:
    return val

def spillargv(argvs, def_conf):
  for argv in argvs:
    # 先截掉最后一个分隔符';'
    argv = cutSuffix(argv)
    # 先判断是否是参数指令
    top = re.search(r_is_params, argv)
    if top:
      top_key = top[1]
      top_val = top[2]
      def_conf[top_key] = {}
      # 判断是否有多层嵌套
      second = re.search(r_multi_params, argv)
      if second:
        __children__(def_conf[top_key], top_val)
      else:
        __evalHandle__(def_conf[top_key], top_val)
  return def_conf

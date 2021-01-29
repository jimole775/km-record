"""
# 指令样例：暂时只支持两层嵌套
# py record match:times=5,interval=0.5 object_name:test
# py record match:False object_name:test1
"""
def spillargv(argvs, def_conf):
  from util.asserts import Assert
  import re
  asserts = Assert()
  for argv in argvs:
    group = re.search(r'(.+):(.+)', arg, re.M|re.I)
    if not group:
      return def_conf
    param_key = group[1]
    param_val = group[2]
    if param_val.index('=') == -1:
      def_conf[param_key] = param_val
    else:
      c_params = param_val.split(',')
      def_conf[param_key] = {}
      for param in c_params:
        c_key = param.split('=')[0]
        c_val = param.split('=')[1]
        if asserts.isNumber(val):
          def_conf[param_key][c_key] = val * 1
        if asserts.isBoolean(val):
          def_conf[param_key][c_key] = eval(val)
        else:
          def_conf[param_key][c_key] = val
  return def_conf
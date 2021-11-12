##############################################
# @exmple: apply(func, (param_a, param_b))
##############################################
def apply (e_instance, e_paramets=()):
    if callable(e_instance):
        __core__(e_instance, e_paramets)

##############################################
# @exmple: call(func, param_a, param_b)
##############################################
def call (e_instance, *e_paramets):
    if callable(e_instance):
        __core__(e_instance, e_paramets)


def __core__ (e_instance, e_paramets):
    param_dict = {}
    # 获取函数的参数数量
    param_cont = e_instance.__code__.co_argcount
    if param_cont > 0 and len(e_paramets) > 0:
        # 获取函数的参数列表
        param_names = e_instance.__code__.co_varnames[0:param_cont]
        i = 0
        for p_name in param_names:
            # 一般情况下，self都是class的成员方法
            if p_name == 'self':
                continue
            # 把参数列表和参数值拼成字典
            param_dict[p_name] = e_paramets[i]
            i = i + 1
    e_instance.__call__(**param_dict)

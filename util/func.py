def apply (e_instance, e_paramets=()):
    if callable(e_instance):
        __core__ (e_instance, e_paramets)


def call (e_instance, *e_paramets):
    if callable(e_instance):
        __core__ (e_instance, e_paramets)

def __core__ (e_instance, e_paramets):
    param_dict = {}
    # 获取函数的参数数量
    param_cont = e_instance.__code__.co_argcount
    if param_cont > 0 and len(e_paramets) > 0:
        # 获取函数的参数列表
        param_names = e_instance.__code__.co_varnames[0:param_cont]
        i = 0
        for p_name in param_names:
            if p_name == 'self':
                continue
            # 把参数列表和参数值拼成字典
            param_dict[p_name] = e_paramets[i]
            i = i + 1
    e_instance.__call__(**param_dict)

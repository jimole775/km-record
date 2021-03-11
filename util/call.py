def call (e_instance, e_paramets=()):
    if callable(e_instance):
        param_dict = {}
        # 获取函数的参数数量
        param_cont = e_instance.__code__.co_argcount
        if param_cont > 0:
            # 获取函数的参数列表
            param_names = e_instance.__code__.co_varnames[0:param_cont]
            i = 0
            for p_name in param_names:
                # 把参数列表和参数值拼成字典
                param_dict[p_name] = e_paramets[i]
                i = i + 1
        e_instance.__call__(**param_dict)
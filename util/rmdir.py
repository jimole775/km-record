# 引入模块
import os
import shutil
def rmdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录不存在')
        return False
    else:
        l_item = os.listdir(path)
        for item in l_item:
            p_item = path + '\\' + item
            if os.path.isdir(item):
                rmdir(p_item)
            else:
                shutil.rmtree(p_item)
        return True
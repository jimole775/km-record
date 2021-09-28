# 字典的值和key进行交换
def swapdict (src):
    if type(src) != dict:
        return src
    result = {}
    for k, v in src.items():
        result[v] = k
    return result
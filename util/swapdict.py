def swapdict (src):
    if type(src) != dict:
        return src
    result = {}
    for k, v in src.items():
        result[v] = k
    return result
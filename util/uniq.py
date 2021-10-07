
def is_uniq(src):
  res = True
  _l = len(src)
  i = 0
  while i < _l:
    if not res:
      break
    item = src[i]
    j = _l - 1
    while j > i:
      jtem = src[j]
      if item == jtem:
        res = False
        break
      j = j - 1
    i = i + 1
  return res

def uniq(src):
  return list(set(src))

if __name__ == "__main__":
  print(uniq([1, 2, 3, 3]))
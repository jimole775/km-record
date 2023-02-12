def call (fn_n, *params):
  fn = eval(fn_n)
  fn(*params)

def test (a, b):
  print(a, b)

def test1 (a, b, c):
  print(a, b, c)

call('test1', 1, 2, 3)
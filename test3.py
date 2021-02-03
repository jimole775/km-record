import sys
import unittest
import keyword
print(keyword.kwlist)
# try
print(sys.platform)
assert ('win32' in sys.platform)
print(sys.argv)
print(sys.path[0])
print(__name__)
print(__builtins__)
print(abs(-123))
print(False)
print(all([1,3,2,5]))
print(any([None,'','','']))
print(__debug__)
class Dad:
    def __init__(self, a):
        print('init:', a)
    def reset(self):
        print('dad:', 1234)
pass
dad = Dad(1000)
class Point(unittest.TestCase, Dad):
    x = 1
    def reset(self, plus):
        super().reset()
pass
a = Point()
a.y = 2
a.name = 'glass'
print(a.x)
a.reset('i ii ')
print(a.x)
print(bool('') == False)
assert 1==True
if(2<2<3): print(1)
else: print(2)
i = 10
while(i>0): i-=1; print(i)
for i in range(10):
    print(i)
dt = dict()
print(dt)
ll = {Ellipsis:1}
print(ll[Ellipsis])
def printinfo(a, *c):
    print(a, c)
pass
printinfo(1,2,3,4,5, {'1':'2'})


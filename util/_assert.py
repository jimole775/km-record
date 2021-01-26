import re
class Assert():
  def isNumber(self, num_like):
    if type(num_like) == str:
      return re.match(r'(^[-\d]\d*(.\d+)?)$', num_like)
  def isBoolean(self, bool_like):
    if type(bool_like) == str:
      return re.match(r'(True|False)', bool_like)
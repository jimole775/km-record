state_record = {
  'test': 1
}

class StateRecord ():
  def get (self, key):
    return state_record[key]

  def set (self, key, value):
    state_record[key] = value

  def delete (self, key):
    del state_record[key]

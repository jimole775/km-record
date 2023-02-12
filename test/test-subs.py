from states.state_record import StateRecord
from states.state_record import state_record
sr = StateRecord()
def test (val):
  print('test', val)
  pass

sr.subscribe('do', test)
sr.set('do', 123)

sr2 = StateRecord()
sr2.subscribe('done', test)
sr2.set('do', 234)
sr2.set('done', 1)

print(state_record)

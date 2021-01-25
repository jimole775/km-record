import sys
DEFAULT = {
  'match_times': 10,
  'match_interval': 0.5,
  'match_click': True,
  'object_name': 'temp',
  'assets_path': '.\\business\\'
}
if len(sys.argv) > 1:
  DEFAULT['object_name'] = sys.argv[1]

class config():
  MATCH_INTERVAL = DEFAULT['match_interval']
  MATCH_CLICK = DEFAULT['match_click']
  MATCH_TIMES = DEFAULT['match_times']
  OBJECT_NAME = DEFAULT['object_name']
  ASSETS_PATH = DEFAULT['assets_path']

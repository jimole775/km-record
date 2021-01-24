import sys
DEFAULT = {
  'match_click': True,
  'object_name': 'temp',
  'assets_path': '.\\business\\'
}
if len(sys.argv) > 1:
  DEFAULT['object_name'] = sys.argv[1]

class config():
  MATCH_CLICK = DEFAULT['match_click']
  OBJECT_NAME = DEFAULT['object_name']
  ASSETS_PATH = DEFAULT['assets_path']

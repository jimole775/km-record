import sys
DEFAULT = {
  'object_name': 'temp',
  'assets_path': '.\\business\\'
}
if len(sys.argv) > 1:
  DEFAULT['object_name'] = sys.argv[1]

class config():
  OBJECT_NAME = DEFAULT['object_name']
  ASSETS_PATH = DEFAULT['assets_path']

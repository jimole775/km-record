'''
 # @ Author: Your name
 # @ Create Time: 2023-02-13 21:44:46
 # @ Modified by: Your name
 # @ Modified time: 2023-02-13 21:44:57
 # @ Description:
 '''

from core.mouse import MouseController
from ui.util.wincompat import px_py_to_html, px_html_to_py

class MoveEvent ():
    def init (self, window):
        self.ctrl = MouseController()
        self.diff_x = 0
        self.diff_y = 0
        self.start_x = 0
        self.start_y = 0
        self.window = window
        pass

    def mount (self, x, y):
        self.ctrl.registe({
            'move': self._move,
            'drop': self._release,
            'release': self._release
        })

        # x, y 对于 py 端来说，就是点击位和左上角的差值
        self._save_diff(x, y)
        self._save_start(x, y)

        # 由于触发事件在前端，此时 press 已经在前端按压了，
        # MoveEvent.mount 时已经不会再有 press 事件触发，
        # 所以这里需要手动加载一次 mouse._press 事件
        self.ctrl.manual_event('press', self.start_x, self.start_y)
        self.ctrl.active()
        pass

    def unmount (self):
        self.ctrl.stop()
        pass

    def _save_diff (self, x, y):
        self.diff_x = x
        self.diff_y = y
        pass

    def _save_start (self, x, y):
        self.start_x = x + self.window.x
        self.start_y = y + self.window.y
        pass

    def _move (self, coord):
        point_x = coord['loc'][0]
        point_y = coord['loc'][1]
        start_x = point_x - px_html_to_py(self.diff_x)
        start_y = point_y - px_html_to_py(self.diff_y)
        self.window.move(start_x, start_y)
        pass

    def _release (self, loc):
        print('release', loc)
        self.unmount()
        pass

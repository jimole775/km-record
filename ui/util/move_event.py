'''
 # @ Author: Your name
 # @ Create Time: 2023-02-13 21:44:46
 # @ Modified by: Your name
 # @ Modified time: 2023-02-13 21:44:57
 # @ Description:
 '''

from core.mouse import MouseController

class MoveEvent ():
    ctrl = MouseController()
    def mount (self):
        self.ctrl.registe({
            'move': self._move,
            'release': self._release
        })
        print('MoveEvent mounted', self.ctrl.is_active)
        self.ctrl.active()
        pass

    def unmount (self):
        self.ctrl.stop()
        pass

    def _move (self, loc):
        print('move:', loc)
        pass

    def _release (self, loc):
        print('release', loc)
        self.unmount()
        pass

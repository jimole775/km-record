state = {
  'test': 1,
  'active': 0, # 0: 线程闲置状态，1: 视图最小化，2: 线程退出
}
subs = {
  'test': None
}

class StateDesktop ():
    def __init__ (self):
        pass

    def subscribe (self, key, callback):
        subs[key] = callback
        pass

    def unsubscribe (self, key):
        del subs[key]
        pass

    def _publish (self, key, value):
        # for item in subs:
        if callable(subs[key]):
            subs[key](value)
        pass

    def delete (self, key):
        del state[key]
        self.unsubscribe(key)
        pass

    def get_state (self, key):
        return state[key]

    def set_state (self, key, value):
        state[key] = value
        self._publish(key, value)
        pass

    def reset_state (self):
        state['active'] = 0
        self._publish('active', 0)
        pass

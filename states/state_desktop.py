state = {
  'active': 0, # 0: 线程闲置状态，1: 视图最小化，2: 线程退出
}
subs = {
  'active': []
}

class StateDesktop ():
    def __init__ (self):
        pass

    def subscribe (self, key, callback):
        self._rise_subs(key, callback)
        pass

    def _rise_subs (self, key, callback):
        try:
            queue = subs[key]
            queue.append(callback)
        except Exception:
            subs[key] = []
            subs[key].append(callback)
        pass

    def _get_subs_queue (self, key):
        try:
            return subs[key]
        except Exception:
            subs[key] = []
            return subs[key]

    def unsubscribe (self, key):
        del subs[key]
        pass

    def _publish (self, key, value):
        subs_queue = self._get_subs_queue(key)
        for sub_item in subs_queue:
            if callable(sub_item):
                sub_item(value)
        pass

    def del_state (self, key):
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
        for key in state:
            val = state[key]
            self._publish(key, val)
        pass

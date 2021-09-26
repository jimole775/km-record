state = {
  'test': 1
}
subs = {
  'test': None
}

class StateDesktop ():
    def __init__(self):
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

    def get (self, key):
        return state[key]

    def set (self, key, value):
        state[key] = value
        self._publish(key, value)
        pass

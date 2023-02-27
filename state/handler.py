from state.play import PLAY_STATE, DEFAULT_PLAY_STATE
from state.record import RECORD_STATE, DEFAULT_RECORD_STATE

class Handler ():
    def __init__ (self):
        pass

    def start (self):
        if PLAY_STATE['idle']:
            PLAY_STATE['working'] = True
            PLAY_STATE['paused'] = False
            PLAY_STATE['idle'] = False
        if RECORD_STATE['idle']:
            RECORD_STATE['working'] = True
            RECORD_STATE['paused'] = False
            RECORD_STATE['idle'] = False
        pass

    def stop (self):
        if not PLAY_STATE['idle']:
            PLAY_STATE['working'] = False
            PLAY_STATE['paused'] = False
            PLAY_STATE['idle'] = True
            self.reset_play_store()
        if not RECORD_STATE['idle']:
            RECORD_STATE['working'] = False
            RECORD_STATE['paused'] = False
            RECORD_STATE['idle'] = True
            self.reset_record_store()
        pass

    def pause (self):
        if PLAY_STATE['working'] and not PLAY_STATE['idle']:
            PLAY_STATE['working'] = False
            PLAY_STATE['paused'] = True

        if RECORD_STATE['working'] and not RECORD_STATE['idle']:
            RECORD_STATE['working'] = False
            RECORD_STATE['paused'] = True
        pass

    def continued (self):
        if PLAY_STATE['paused'] and not PLAY_STATE['idle']:
            PLAY_STATE['working'] = True
            PLAY_STATE['paused'] = False

        if RECORD_STATE['paused'] and not RECORD_STATE['idle']:
            RECORD_STATE['working'] = True
            RECORD_STATE['paused'] = False
        pass

    def update_step (self):
        if PLAY_STATE['working']:
            PLAY_STATE['step'] += 1
        if RECORD_STATE['working']:
            RECORD_STATE['step'] += 1
        pass

    def get_play_store (self, key):
        return PLAY_STATE[key]

    def get_record_store (self, key):
        return RECORD_STATE[key]

    def set_play_store (self, key, value):
        PLAY_STATE[key] = value
        pass

    def set_record_store (self, key, value):
        RECORD_STATE[key] = value
        pass

    def reset_play_store (self):
        for key in DEFAULT_PLAY_STATE:
            PLAY_STATE[key] = DEFAULT_PLAY_STATE[key]
        pass

    def reset_record_store (self):
        for key in DEFAULT_RECORD_STATE:
            RECORD_STATE[key] = DEFAULT_RECORD_STATE[key]
        pass

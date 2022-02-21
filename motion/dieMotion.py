from motion.motion import *


class DieMotion(Motion):
    def __init__(self, time):
        super().__init__((time, None))

    def getpos(self):
        t = self.get_valid_time()
        if t <= 0:
            return vector(0, 0)
        return None

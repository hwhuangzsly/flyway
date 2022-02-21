from motion.motion import *


class LineMotion(Motion):
    def __init__(self, theta, s, interval=(None, None)):
        super().__init__(interval)
        self.s = s
        self.theta = theta

    def getpos(self):
        t = self.get_valid_time()
        l = self.s(t)
        return vector(l * math.cos(self.theta), l * math.sin(self.theta))
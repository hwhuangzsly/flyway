from motion.motion import *


class CircleMotion(Motion):
    def __init__(self, o, r=lambda t: 0.0, theta=lambda t: 0.0, interval=(None, None)):
        super().__init__(interval)
        self.o = o
        self.theta = theta
        self.r = r
        self.init_r = None
        self.init_theta = None
        self.init_pos = None

    def getpos(self):
        t = self.get_valid_time()
        if t <= 0:
            return vector(0, 0)
        if self.init_r is None:
            self.init_pos = self.parent.pos.copy()
            self.init_theta = get_theta(self.o, self.parent.pos)
            self.init_r = district(self.o, self.parent.pos)
        theta = self.theta(t) + self.init_theta
        r = self.r(t) + self.init_r
        return r * vector(math.cos(theta), math.sin(theta)) - self.init_pos + self.o

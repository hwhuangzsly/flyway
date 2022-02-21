import math

from motion.motion import *


class RectRandomMotion(Motion):

    def __init__(self, x1, y1, x2, y2, freq=100, v=3, interval=(None, None)):
        super().__init__(interval)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.freq = freq
        self.left_freq = freq
        self.v = v
        self.left_goal = 0
        self.theta = None

    def get_delta_pos(self):
        if not self.valid():
            return vector(0, 0)
        if self.left_freq <= 0:
            x = random.uniform(self.x1, self.x2)
            y = random.uniform(self.y1, self.y2)
            self.theta = get_theta(self.parent.init_pos, vector(x, y))
            self.left_goal = district(self.parent.init_pos, vector(x, y))
            self.left_freq = self.freq
        elif self.left_goal <= 0:
            self.left_freq -= 1
        else:
            self.left_goal -= self.v
            return self.v * vector(math.cos(self.theta), math.sin(self.theta))
        return vector(0, 0)

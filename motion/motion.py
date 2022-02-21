from lifetime import *


class Motion(Lifetime):

    def __init__(self, interval):
        super().__init__(interval)
        self.parent = None

    def getpos(self):
        return vector(0, 0)

    def get_delta_pos(self):
        return vector(0, 0)

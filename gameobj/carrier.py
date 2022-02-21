from gameobj.gameObj import *


class Carrier(GameObj):
    def __init__(self, init_pos, friendly=False, one_off=False, reflect_flag=(False, False, False, False), reflect_time=float('inf')):
        super().__init__(init_pos, friendly=friendly, reflect_flag=reflect_flag, reflect_time=reflect_time)
        self.one_off = one_off
        self.modes = []
        self.obj = pygame.Surface((10, 10))
        self.obj.fill((255, 255, 255,))
        pygame.draw.rect(self.obj, (0, 0, 0,), (0, 0, 10, 10), 10)

    def add_mode(self, mode):
        mode.set_parent(self)
        self.modes.append(mode)
        return self

    def update_carrier(self):
        self.update_pos()
        shot = False
        for mode in self.modes:
            if mode.check():
                shot = True
                if self.one_off:
                    self.alive = False
        return shot
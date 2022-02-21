from gameobj.carrier import *

class Bullet(Carrier):
    def __init__(self, init_pos, friendly=False, reflect_flag=(False, False, False, False), reflect_time=float('inf')):
        super().__init__(init_pos, friendly=friendly, reflect_flag=reflect_flag, reflect_time=reflect_time)
        self.obj = pygame.Surface((10, 10))
        self.obj.fill((255, 255, 255,))
        pygame.draw.circle(self.obj, (255, 0, 0,), (5, 5), 5, 0)

    def update(self):
        self.update_carrier()
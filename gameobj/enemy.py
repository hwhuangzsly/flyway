from gameobj.carrier import *


class Enemy(Carrier):
    def __init__(self, init_pos, one_off=False, life_point=10, boss=False, reflect_flag=(False, False, False, False), reflect_time=float('inf')):
        super().__init__(init_pos, one_off=one_off, reflect_flag=reflect_flag, reflect_time=reflect_time)
        self.life_point = life_point
        self.boss = boss

    def update(self):
        pass

    def accept_damage(self, damage):
        self.life_point -= damage
        if self.life_point <= 0:
            self.alive = False


class MajorEnemy(Enemy):
    def __init__(self, init_pos, one_off=False, life_point=10, boss=False, reflect_flag=(False, False, False, False), reflect_time=float('inf')):
        super(MajorEnemy, self).__init__(init_pos, one_off=one_off, life_point=life_point, boss=boss, reflect_flag=reflect_flag, reflect_time=reflect_time)
        self.secondary_enemy_creators = []
        self.secondary_enemies = []
        self.obj = pygame.Surface((10, 10))
        self.obj.fill((255, 255, 255,))
        pygame.draw.rect(self.obj, (0, 0, 0,), (0, 0, 10, 10), 10)

    def add_secondary_enemy_creator(self, secondary_enemy_creator):
        self.secondary_enemy_creators.append(secondary_enemy_creator)
        return self

    def update(self):
        shot = self.update_carrier()
        if shot and len(self.secondary_enemies) == 0:
            for creator in self.secondary_enemy_creators:
                secondary_enemy = creator(self)
                secondary_enemy.set_parent(self)
                self.secondary_enemies.append(secondary_enemy)


class SecondaryEnemy(Enemy):
    def __init__(self, init_pos, one_off=False, life_point=10, boss=False, reflect_flag=(False, False, False, False), reflect_time=float('inf')):
        super(SecondaryEnemy, self).__init__(init_pos, one_off=one_off, life_point=life_point, boss=boss, reflect_flag=reflect_flag, reflect_time=reflect_time)
        self.parent = None
        self.parent_last_pos = None
        self.obj = pygame.Surface((10, 10))
        self.obj.fill((255, 255, 255,))
        pygame.draw.rect(self.obj, (0, 0, 255,), (0, 0, 10, 10), 10)

    def set_parent(self, parent):
        self.parent = parent
        self.parent_last_pos = parent.pos.copy()

    def update(self):
        self.init_pos += (self.parent.pos - self.parent_last_pos)
        self.parent_last_pos = self.parent.pos.copy()
        self.update_carrier()


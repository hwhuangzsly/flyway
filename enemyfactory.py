import math
import random

from gameobj.enemy import *
from mode.mode import *


class EnemyFactory:
    @staticmethod
    def create(enemy_name, *args, **kwargs):
        return getattr(EnemyFactory, enemy_name)(*args, **kwargs)

    # 从x1, y1到x2, y2,期间进行自机射击
    @staticmethod
    def enemy1(x1, y1, x2, y2):
        theta = get_theta(vector(x1, y1), vector(x2, y2))
        return MajorEnemy(vector(x1, y1)).add_mode(AimMode(5, freq=10)).add_motion(LineMotion(theta, lambda t: 2*t))

    # 从(x1,0)至(x1,y1)后，开始进行自机射击,进行1次扩散射击等待t帧,随后向(x2, y2)离开
    @staticmethod
    def enemy2(x1, y1, x2, y2, t):
        v = 4
        begin_shot = y1/v
        return MajorEnemy(vector(x1, 0)).add_motion(LineMotion(math.pi/2, lambda t: v*t, interval=(None, begin_shot)))\
            .add_mode(AimMode(2, n=2, freq=50, interval=(begin_shot, None)))\
            .add_mode(SpreadMode(40, 20, lambda t: 2*t, freq=200, interval=(begin_shot, begin_shot+t)))\
            .add_motion(LineMotion(get_theta(vector(x1, y1), vector(x2, y2)), lambda t: v/2 * t, interval=(begin_shot+t, None)))

    # 从x1, y1到x2, y2后,进行1次自机射击等待t帧，随后返回x1, y1离开，该坐标附加小范围扰动
    @staticmethod
    def enemy3(x1, y1, x2, y2, t):
        v = 4
        diff = 20
        x3 = x1 + random.uniform(-diff, diff)
        y3 = y1 + random.uniform(-diff, diff)
        x2 += random.uniform(-diff, diff)
        y2 += random.uniform(-diff, diff)
        begin_shot = district(vector(x1, y1), vector(x2, y2))/v
        return MajorEnemy(vector(x1, y1)).add_motion(LineMotion(get_theta(vector(x1, y1), vector(x2, y2)), lambda t: v * t, interval=(None, begin_shot))) \
            .add_mode(AimMode(2, interval=(begin_shot, begin_shot + t))) \
            .add_motion(LineMotion(get_theta(vector(x2, y2), vector(x3, y3)), lambda t: v/2 * t, interval=(begin_shot + t, None)))

    # 从(x1,0)至(x1,y1)后，进行1次扩散射击召唤4只围绕在身边的使魔进行自机射击，等待t帧,随后向(x2, y2)离开
    @staticmethod
    def enemy4(x1, y1, x2, y2, t):
        v = 4
        begin_shot = y1 / v
        enemy = MajorEnemy(vector(x1, 0)).add_motion(LineMotion(math.pi / 2, lambda t: v * t, interval=(None, begin_shot))) \
            .add_mode(SpreadMode(40, 20, lambda t: 2 * t, freq=200, interval=(begin_shot, begin_shot + t))) \
            .add_motion(LineMotion(get_theta(vector(x1, y1), vector(x2, y2)), lambda t: v / 2 * t, interval=(begin_shot + t, None)))
        for i in range(4):
            theta = (2*i+1)*math.pi/4
            enemy.add_secondary_enemy_creator(lambda m, _theta=theta: SecondaryEnemy(m.pos + 50*vector(math.cos(_theta), math.sin(_theta))) \
            .add_motion(CircleMotion(m.pos.copy(), theta=lambda t: 0.05*t)).add_mode(AimMode(2, freq=50, interval=(50, None))))
        return enemy

    @staticmethod
    def spell_card_1_1():
        enemy = MajorEnemy(vector(300, 200), life_point=100, boss=True).add_realtime_motion(RectRandomMotion(100, 100, 500, 200))
        for i in range(4):
            enemy.add_mode(Sector90(5, 1+i*5, 50+i*5, 2, freq=200))
        return enemy

    @staticmethod
    def spell_card_1():
        return MajorEnemy(vector(300, 200), life_point=100, boss=True).add_mode(ReflectMode(300, 10, 0.03, lambda t: 5*t, freq=200, interval=(60, None)))\
            .add_mode(SpreadMode(40, 20, lambda t: 2*t, freq=50, interval=(60, None)))\
            .add_realtime_motion(RectRandomMotion(100, 100, 500, 300))

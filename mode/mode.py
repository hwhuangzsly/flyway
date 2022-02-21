import math

from gameobj.bullet import *
from motion.lineMotion import *
from motion.circleMotion import *
from motion.dieMotion import *
from motion.rectRandomMotion import *
from lifetime import *


class Mode(Lifetime):
    def __init__(self, interval, freq):
        super().__init__(interval)
        self.freq = freq
        self.init = False
        self.parent = None

    def create_bullets(self):
        return []

    def set_parent(self, parent):
        self.parent = parent

    def available(self):
        return True

    def check(self):
        t = self.get_relative_time()
        bullets = []
        if not self.available():
            return False
        if self.freq is not None:
            if self.valid() and t % self.freq == 0:
                bullets = list(self.create_bullets())
                Properties.bullets.extend(bullets)
        else:
            if t >= 0 and not self.init:
                bullets = list(self.create_bullets())
                Properties.bullets.extend(self.create_bullets())
                if (len(bullets)) > 0:
                    self.init = True
        return len(bullets) > 0

    def __copy__(self):
        pass

    def copy(self):
        return self.__copy__()



class SpreadMode(Mode):
    def __init__(self, n, r, s, init_theta=0.0, limit_t=None, interval=(None, None), freq=None):
        super().__init__(interval, freq)
        self.n = n
        self.r = r
        self.s = s
        self.init_theta = init_theta
        self.limit_t = limit_t

    def create_bullets(self):
        theta = 2 * math.pi / self.n
        for i in range(self.n):
            last_theta = i * theta + self.init_theta
            bullet = Bullet(self.r * vector(math.cos(last_theta), math.sin(last_theta)) + self.parent.pos).add_motion(LineMotion(last_theta, self.s))
            if self.limit_t is not None:
                bullet.add_motion(DieMotion(self.limit_t))
            yield bullet

    def __copy__(self):
        return SpreadMode(self.n, self.r, self.s, self.init_theta, self.limit_t, self.interval, self.freq)


class CircleSpreadMode(Mode):
    def __init__(self, n, r, tr, vr, init_theta=0.0, interval=(None, None), freq=None):
        super().__init__(interval, freq)
        self.n = n
        self.r = r
        self.tr = tr
        self.vr = vr
        self.init_theta = init_theta

    def create_bullets(self):
        theta = 2 * math.pi / self.n
        for i in range(self.n):
            last_theta = i * theta + self.init_theta
            yield Bullet(self.parent.pos).add_motion(LineMotion(last_theta, lambda t: self.r/self.tr*t, interval=(0, self.tr)))\
                .add_motion(CircleMotion(self.parent.pos, r=lambda t: t, theta=lambda t: self.vr*t, interval=(self.tr+50, None)))

    def __copy__(self):
        return CircleSpreadMode(self.n, self.r, self.tr, self.vr, self.init_theta, self.interval, self.freq)

class ReflectMode(Mode):
    def __init__(self, h, n, theta, s, interval=(None, None), freq=None):
        super().__init__(interval, freq)
        self.h = h
        self.n = n
        self.theta = theta
        self.s = s

    def create_bullets(self):
        last_theta = random.uniform(-self.theta, self.theta) + math.pi/2
        d = Properties.width / self.n
        for i in range(2 * self.n):
            yield Bullet(vector(-Properties.width/2 + d*i, self.h), reflect_flag=(1, 1, 0, 0), reflect_time=10).add_motion(LineMotion(last_theta, self.s))

    def __copy__(self):
        return ReflectMode(self.h, self.n, self.theta, self.interval, self.freq)


class AimMode(Mode):
    def __init__(self, v, n=1, stop=False, interval=(None, None), freq=None):
        super().__init__(interval, freq)
        self.v = v
        self.stop = stop
        self.n = n

    def create_bullets(self):
        sub = Properties.me - self.parent.pos
        last_theta = get_theta(self.parent.pos, Properties.me)
        if not self.stop:
            t = None
        else:
            t = math.sqrt(sub.x**2+sub.y**2)/self.v
        for i in range(-self.n+1, self.n):
            yield Bullet(self.parent.pos).add_motion(LineMotion(last_theta + i * 0.1, lambda t: self.v*t, interval=(None, t)))

    def __copy__(self):
        return AimMode(self.v, self.stop, self.interval, self.freq)


class RepeatMode(Mode):
    def __init__(self, mode1, mode2, repeat_times, depth=0, condition=None, one_off=False):
        super().__init__(mode1.interval, mode1.freq)
        self.mode1 = mode1
        self.mode2 = mode2
        self.repeat_times = repeat_times
        self.condition = condition
        self.depth = depth
        self.one_off = one_off

    def set_parent(self, parent):
        self.mode1.parent = parent

    def available(self):
        if self.depth != 1 or self.condition is None or self.condition(self.mode2.parent):
            return True
        self.init_time = Properties.time
        return False

    def create_bullets(self):
        if self.repeat_times >= 0:
            for bullet in self.mode1.create_bullets():
                bullet.one_off = self.one_off
                mode = self.mode2.copy()
                yield bullet.add_mode(RepeatMode(mode, mode, self.repeat_times - 1, depth=self.depth+1, condition=self.condition, one_off=self.one_off))


class Sector90(Mode):
    def __init__(self, n, t1, t2, v, interval=(None, None), freq=None):
        super().__init__(interval, freq)
        self.n = n
        self.t1 = t1
        self.t2 = t2
        self.v = v
        self.dir = 1

    def create_bullets(self):
        direct = get_theta(self.parent.pos, Properties.me)-self.dir*math.pi/2
        for i in range(-self.n+1, self.n):
            theta = direct + i * 0.3
            yield Bullet(self.parent.pos).add_motion(LineMotion(theta, lambda t: self.v * t, interval=(None, self.t1)))\
                .add_motion(LineMotion(theta+self.dir*math.pi/2, lambda t: self.v * t, interval=(self.t2, None)))
        self.dir *= -1




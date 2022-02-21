from properties import *


class GameObj:
    def __init__(self, init_pos, friendly=False, reflect_flag=(False, False, False, False), reflect_time=float('inf')):
        self.pos = init_pos
        self.init_pos = init_pos.copy()
        self.motions = []
        self.realtime_motions = []
        self.reflect_flag = reflect_flag
        self.reflect_time = reflect_time
        self.alive = True
        self.friendly = friendly

    def add_motion(self, motion):
        motion.parent = self
        self.motions.append(motion)
        return self

    def add_realtime_motion(self, motion):
        motion.parent = self
        self.realtime_motions.append(motion)
        return self

    @staticmethod
    def stop(game_obj):
        stop = True
        for motion in game_obj.motions:
            if motion.valid():
                stop = False
                return stop
        return stop


    def update_pos(self):
        # 根据每个参考系计算坐标最后相加
        for motion in self.realtime_motions:
            motion_pos = motion.get_delta_pos()
            self.init_pos += motion_pos
        self.pos = self.init_pos.copy()
        for motion in self.motions:
            motion_pos = motion.getpos()
            if motion_pos is None:
                self.alive = False
                return
            self.pos += motion_pos
        # 处理反射,终止反射的条件：没有反射面 或 反射次数为0
        reflect_time = self.reflect_time
        while reflect_time > 0:
            x = self.pos.x
            y = self.pos.y
            xa = None
            ya = None
            if x > Properties.width and self.reflect_flag[3]:
                xa = Properties.width
            elif x < 0 and self.reflect_flag[2]:
                xa = 0
            if y > Properties.height and self.reflect_flag[1]:
                ya = Properties.height
            elif y < 0 and self.reflect_flag[0]:
                ya = 0
            if xa is None and ya is None:
                break
            if xa is not None:
                self.pos.x = 2 * xa - x
                reflect_time -= 1
                if reflect_time <= 0:
                    break
            if ya is not None:
                self.pos.y = 2 * ya - y
                reflect_time -= 1
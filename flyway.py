from mode.mode import *
from gameobj.enemy import *
from enemyfactory import *

scaling_factor = 1.5
pygame.init()
# 初始化用于显示的窗口并设置窗口尺寸
win = pygame.display.set_mode((int(Properties.width*scaling_factor), int(Properties.height*scaling_factor)))
screen = pygame.Surface((Properties.width, Properties.height))
# 设置当前窗口的标题
pygame.display.set_caption('飞机')
clock = pygame.time.Clock()


# Properties.enemies = [Enemy(vector(300, 450)).add_mode(AimMode(5, freq=10, interval=(0, 60)))
#                           .add_mode(SpreadMode(80, 20, lambda t: 3*t, 0.12, freq=20, interval=(60, 120)))
#                           .add_mode(AimMode(5, freq=10, interval=(120, None)))
#                           .add_motion(LineMotion(0.5, lambda t:0.5*t))]
#
# Properties.enemies = [Enemy(vector(300, 450)).add_mode(RepeatMode(AimMode(5, freq=50, interval=(60, None), stop=True),
#                                                                   SpreadMode(5, 50, lambda t: t, 0.12, freq=None, interval=(30, None), limit_t=40), 2,
#                                                                   condition=GameObj.stop, one_off=True))]


def bullet_valid(bullet):
    if not bullet.alive:
        return False
    point = bullet.pos
    buffer = 200
    if point.x < -buffer or point.x > Properties.width + buffer or point.y > Properties.height + buffer or point.y < -buffer:
        return False
    return True


def enemy_valid(enemy):
    if not enemy.alive:
        return False
    point = enemy.pos
    buffer = 50
    if point.x < -buffer or point.x > Properties.width + buffer or point.y > Properties.height + buffer or point.y < -buffer:
        return False
    return True


def get_all_secondary_enemies(enemies):
    result = []
    for enemy in enemies:
        result.extend(filter(lambda x: x.alive, enemy.secondary_enemies))
    return result


def move():
    secondary_enemies = get_all_secondary_enemies(Properties.enemies)
    for enemy in Properties.enemies:
        enemy.update()
    for enemy in secondary_enemies:
        enemy.update()

    bullets = Properties.bullets.copy()
    for bullet in bullets:
        bullet.update()

    # 自机碰撞判定
    # for bullet in Properties.bullets:
    #     if bullet_valid(bullet) and not bullet.friendly and conflict(Properties.me, bullet.pos, 10):
    #         bullet.alive = False
    #         Properties.running = False
    #         return

    # 敌机中弹判定
    for enemy in Properties.enemies + secondary_enemies:
        for bullet in Properties.bullets:
            if enemy_valid(enemy) and bullet_valid(bullet) and bullet.friendly and conflict(enemy.pos, bullet.pos, 10):
                enemy.accept_damage(1)
                bullet.alive = False

    for enemy in Properties.enemies:
        if not enemy_valid(enemy):
            Properties.enemies.remove(enemy)
            if enemy.boss:
                Properties.timeline.insert(0, (-1, 0))

    for bullet in Properties.bullets:
        if not bullet_valid(bullet):
            Properties.bullets.remove(bullet)

    # 设置窗口的背景色(颜色是由红绿蓝三原色构成的元组)
    screen.fill((242, 242, 242))
    """Draw screen objects."""
    screen.blit(Properties.meObj, (Properties.me.x, Properties.me.y))

    for enemy in Properties.enemies + secondary_enemies:
        screen.blit(enemy.obj, (enemy.pos.x, enemy.pos.y))

    for bullet in Properties.bullets:
        screen.blit(bullet.obj, (bullet.pos.x, bullet.pos.y))
    win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))


def clear():
    clear_bullets()
    Properties.enemies.clear()
    Properties.last_clear_time = Properties.time


def clear_bullets():
    Properties.bullets.clear()


def main():
    running = True
    xv = 0
    yv = 0
    slow = False
    shot = False
    freq = 1
    left_freq = 0
    timeline = Properties.timeline
    maxtime = 0
    timeline.append((1, 1, 'spell_card_1_1'))
    # for i in range(6):
    #     timeline.append((20*i, 1, 'enemy3', Properties.width//6, 0, Properties.width//4, Properties.height//3, 20))
    # for i in range(11, 17):
    #     timeline.append((20*i, 1, 'enemy3', Properties.width//6, 0, Properties.width//4, Properties.height//3, 20))
    # for i in range(22, 34):
    #     timeline.append((20*i, 1, 'enemy3', 5*Properties.width//6, 0, 3*Properties.width//4, Properties.height//3, 20))
    # timeline.append((750, 1, 'enemy2', Properties.width//3, Properties.height//4, Properties.width, Properties.height//2, 150))
    # timeline.append((900, 1, 'enemy2', 2*Properties.width//3, Properties.height//4, 0, Properties.height//2, 150))
    # for i in range(50, 56):
    #     timeline.append((20*i, 1, 'enemy3', Properties.width//6, 0, Properties.width//4, Properties.height//4, 20))
    # for i in range(56, 62):
    #     timeline.append((20*i, 1, 'enemy3', 5*Properties.width//6, 0, 3*Properties.width//4, Properties.height//3, 20))
    # timeline.append((1300, 1, 'enemy2', Properties.width//3, Properties.height//4, Properties.width, Properties.height//2, 150))
    # timeline.append((1300, 1, 'enemy4', 2*Properties.width//3, Properties.height//4, 0, Properties.height//2, 200))
    # timeline.append((1550, 1, 'enemy4', Properties.width // 3, Properties.height // 4, Properties.width, Properties.height // 2, 200))
    # timeline.append((1550, 1, 'enemy2', 2 * Properties.width // 3, Properties.height // 4, 0, Properties.height // 2, 150))
    # for i in range(80, 86):
    #     timeline.append((20*i, 1, 'enemy3', Properties.width//6, 0, Properties.width//4, Properties.height//4, 20))
    # for i in range(86, 92):
    #     timeline.append((20*i, 1, 'enemy3', 5*Properties.width//6, 0, 3*Properties.width//4, Properties.height//3, 20))
    # for i in range(92, 98):
    #     timeline.append((20*i, 1, 'enemy3', Properties.width//6, 0, Properties.width//4, Properties.height//4, 20))
    # for i in range(98, 104):
    #     timeline.append((20*i, 1, 'enemy3', 5*Properties.width//6, 0, 3*Properties.width//4, Properties.height//3, 20))
    # timeline.append((2100, 1, 'enemy2', Properties.width // 3, Properties.height // 4, Properties.width, Properties.height // 2, 150))
    # timeline.append((2100, 1, 'enemy2', 2 * Properties.width // 3, Properties.height // 4, 0, Properties.height // 2, 150))
    while running:
        clock.tick(60)
        v = 5
        # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xv += -v
                elif event.key == pygame.K_RIGHT:
                    xv += +v
                elif event.key == pygame.K_UP:
                    yv += -v
                elif event.key == pygame.K_DOWN:
                    yv += +v
                elif event.key == pygame.K_LSHIFT:
                    slow = True
                elif event.key == pygame.K_z:
                    shot = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    xv -= -v
                if event.key == pygame.K_RIGHT:
                    xv -= +v
                elif event.key == pygame.K_UP:
                    yv -= -v
                elif event.key == pygame.K_DOWN:
                    yv -= +v
                elif event.key == pygame.K_LSHIFT:
                    slow = False
                elif event.key == pygame.K_z:
                    shot = False
                elif event.key == pygame.K_RETURN:
                    if not Properties.running:
                        clear_bullets()
                        Properties.running = True
        if not Properties.running:
            continue
        if slow:
            Properties.me.x += xv/2
            Properties.me.y += yv/2
        else:
            Properties.me.x += xv
            Properties.me.y += yv
        # 自机射击 todo 自机的移动和射击等行为应和敌机一起处理
        if shot:
            if left_freq <= 0:
                left_freq = freq
                Properties.bullets.append(Bullet(Properties.me, friendly=True).add_motion(LineMotion(1.5*math.pi, lambda t: 10*t)))
            else:
                left_freq -= 1
        if len(timeline) > 0 and (maxtime <= timeline[0][0]+Properties.last_clear_time <= Properties.time or timeline[0][0] < 0):
            maxtime = timeline[0][0] + Properties.last_clear_time
            event_type = timeline[0][1]
            if event_type == 0:
                while len(timeline) > 0 and timeline[0][1] == 0:
                    del timeline[0]
                clear()
            elif event_type == 1:
                enemy_type = timeline[0][2]
                Properties.enemies.append(EnemyFactory.create(enemy_type, *timeline[0][3:]))
                del timeline[0]
        move()
        pygame.display.update()
        Properties.time += 1


if __name__ == '__main__':
    main()


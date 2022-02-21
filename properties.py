import pygame
import math
import random
from utils import vector, get_theta, conflict, district


class Properties:
    width = 600
    height = 600
    time = 0
    last_clear_time = 0
    running = True
    bullets = []
    enemies = []
    timeline = []
    me = vector(300, 500)
    meObj = pygame.Surface((10, 10))
    meObj.fill((255, 255, 255,))
    pygame.draw.rect(meObj, (0, 255, 0,), (0, 0, 10, 10), 10)

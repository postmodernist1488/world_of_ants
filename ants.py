import pyglet
from event import EventHook
from collections import deque
from pyglet import clock
import random
from math import cos, sin, radians

class Ants(pyglet.sprite.Sprite):
    def __init__(self, gm_x:int, gm_y:int, gm_scale:int, game_map=None, batch = None, group = None):
        self.gm_x = gm_x
        self.gm_y = gm_y
        self.game_map = game_map
        self.gm_scale = gm_scale
        
        image_frames_ant = ('images/ant_ani_01.png', 'images/ant_ani_03.png','images/ant_ani_02.png','images/ant_ani_03.png')
        images_ant = []
        for i in image_frames_ant:
            img = pyglet.image.load(i)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
            images_ant.append(img)        
        animation_ant = pyglet.image.Animation.from_image_sequence(images_ant, 0.2, True)

        super(Ants, self).__init__(animation_ant, x = gm_x * gm_scale + gm_scale / 2, y=gm_y * gm_scale + gm_scale / 2, batch = batch, group= group)
        self.on_create = EventHook()
        self.on_destroy = EventHook()
        self.deque_move()
        self.rotation = 0 #начальный угол
        self.direction_move = 0 #
        self.target_d = 0 #целевой угол поворота
        self.cw = 1 #направление по часовой/против часовой стрелки
        #########
        self.dist = 0 #целевое количество шагов
        self.step = 0 #текущий шаг
        self.next_step = {0: (0, 1), 
                         45: (1, 1), 
                         90: (1, 0),
                         135: (1, -1),
                         180: (0, -1),
                         225: (-1, -1),
                         270: (-1, 0),
                         315: (-1, 1)}

    def create(self):
        self.on_create.fire()
        clock.schedule_interval(self.move_ant, 1/60)

    def move_ant(self, dt):
        self.q_state[0]()
        

    def deque_move(self):
        self.q_state = deque([self.prepare_ant, self.rotate_ant, self.step_ant])
        
    def prepare_ant(self):
        self.direction_move = random.randrange(0, 181, 45)
        self.cw = random.choice([-1, 1])
        self.target_d = (self.rotation + self.direction_move * self.cw) % 360
        self.q_state.rotate(-1)
        self.step = 0
        self.dist = random.randrange(10, 51, 10)


    def rotate_ant(self):
        if (self.rotation) % 360 != self.target_d:
            self.rotation = (self.rotation + 5 * self.cw) % 360
        else:
            self.q_state.rotate(-1)

    def step_ant(self):
        if self.step < self.dist:
            rad = radians(90 - self.rotation)
            self.x += cos(rad)
            self.y += sin(rad)
            self.step += 1    
        else:
            self.q_state.rotate(-1)


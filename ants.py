import pyglet
from event import EventHook
from collections import deque
from pyglet import clock
import random
import math

SQRT_2 = 1.41421356237

class Ants(pyglet.sprite.Sprite):
    def __init__(self, gm_x: int , gm_y: int, batch = None, group = None, game_map = None):
        self.gm_x = gm_x
        self.gm_y = gm_y
        self.game_map = game_map
        self.gm_scale = game_map.scale
        image_frames_ant = ('images/ant_ani_01.png', 'images/ant_ani_03.png','images/ant_ani_02.png','images/ant_ani_03.png')
        images_ant = []
        for i in image_frames_ant:
            img = pyglet.image.load(i)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
            images_ant.append(img)        
        animation_ant = pyglet.image.Animation.from_image_sequence(images_ant, 0.2, True)

        super(Ants, self).__init__(animation_ant, x = gm_x*self.gm_scale+self.gm_scale/2, y=gm_y*self.gm_scale + self.gm_scale/2, batch = batch, group= group)
        self.scale = self.gm_scale / 20
        self.on_create = EventHook()
        self.on_destroy = EventHook()
        self.deque_move()

        self.rotation = 0 # начальное расположение (угол)
        self.direction_move = 0 # на сколько градусов хочу повернуть
        self.target_d = 0 # целевой угол поворота (0 сверху)
        self.cw = 1 # направление поворота

        self.dist = 0 # целевое количество шагов
        self.step = 0 # текущий шаг
        self.next_step = { 0:(0, 1), 45:(1, 1), 90:(1, 0), 135:(1, -1), 180:(0, -1), 225:(-1, -1), 270:(-1, 0), 315:(-1,1)  }

    def create(self):
        self.on_create.fire()
        clock.schedule_interval(self.move_ant, 1/60)       

    def move_ant(self, dt):
        self.q_state[0]()

    def deque_move(self):
        self.q_state = deque()
        self.q_state.append(self.prepare_ant)
        self.q_state.append(self.rotate_ant)
        self.q_state.append(self.step_ant)

    def prepare_ant(self):
        self.direction_move = random.randrange(0, 181, 45)
        self.cw = random.choice([-1, 1]) # против / по часовой стрелке
        self.target_d = (self.rotation + self.direction_move * self.cw) % 360

        self.step = 0 
        #self.dist = random.randrange(10, 51, 10)
        self.dist = self.gm_scale

        #получить адрес следующей игровой клетки
        self.gm_x_next = self.gm_x + self.next_step[self.target_d][0]
        self.gm_y_next = self.gm_y + self.next_step[self.target_d][1] 

        if self.game_map.map_list[self.gm_y_next][self.gm_x_next] == 0:
            self.x_dest = self.gm_x_next * self.gm_scale + self.gm_scale/2
            self.y_dest = self.gm_y_next * self.gm_scale + self.gm_scale/2
            self.q_state.rotate(-1)

    def rotate_ant(self):
        if (self.rotation)% 360 !=  self.target_d:
            self.rotation = (self.rotation + 5 * self.cw ) % 360
        else:
            self.q_state.rotate(-1)

    def step_ant(self):
        if self.step < self.dist:
            self.step += 1
            rad = math.radians((360 + 90 - self.rotation) % 360)
            if self.rotation % 90 == 0:
                self.x += math.cos(rad)
                self.y += math.sin(rad)
            else:
                self.x += math.cos(rad) * SQRT_2
                self.y += math.sin(rad) * SQRT_2

        else:
            self.x = self.x_dest
            self.y = self.y_dest
            self.gm_x = self.gm_x_next
            self.gm_y = self.gm_y_next

            tile_idx = self.gm_y * self.game_map.count_x + self.gm_x
            self.game_map.tile_list[tile_idx].new_track(2)
            self.q_state.rotate(-1)

    def destroy(self):                     
            clock.unschedule(self.move_ant) #Отмена таймера
            self.batch = None #Исключаем из пачки
            self.on_destroy.fire()
            self.delete() #суицид  

    def __del__(self):
        print('Ant destroyed') #проверка смерти
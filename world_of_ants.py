import pyglet
from pyglet import clock
from pyglet.gl import *
from ants import Ants
from pyglet.window import key, Window
from backdrop import *



class Game_Window(Window):
    def __init__(self):
        super(Game_Window,self).__init__(1366,768, "Симулятор муравейника")
        self.opengl_init()
        self.batch_01 = pyglet.graphics.Batch()
        self.layer_00 = pyglet.graphics.OrderedGroup(0)
        self.layer_01 = pyglet.graphics.OrderedGroup(1)
        self.layer_02 = pyglet.graphics.OrderedGroup(2)
        self.alive = 1
        self.gm_scale = 10
        self.game_map = Game_Map(self.gm_scale, batch=self.batch_01, group=self.layer_01)
        self.game_map.fill()
        self.x_offset = 0
        self.y_offset = 0

    def opengl_init(self):
        glClearColor(255.0/255.0, 255.0/255.0, 255.0/255.0, 1) # цвет окна
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthFunc(GL_LEQUAL)

    def render(self):
        self.clear()
        self.batch_01.draw()
        self.flip()
    
    def on_close(self):
        self.alive = 0

    def run(self):
        while self.alive == 1:
            self.render()
            dt = clock.tick() # тикаем часиками
            event = self.dispatch_events() # опрашиваем события 
    
    def create_ant(self, x, y):
        new_ant = Ants(gm_x= int(x // self.gm_scale), gm_y=int(y // self.gm_scale), batch=self.batch_01, group=self.layer_02, game_map=self.game_map)
        new_ant.create()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LCTRL:
            self.create_ant(100, 100)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            
            self.create_ant(x - self.x_offset, y - self.y_offset)


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == pyglet.window.mouse.MIDDLE:
            glTranslatef(-dx, -dy, 0)
            self.x_offset -= dx
            self.y_offset -= dy



game_window = Game_Window()

game_window.run()
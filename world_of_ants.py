import pyglet
from pyglet import clock
from pyglet.gl import *
from ants import Ants
from pyglet.window import key, Window


class Game_Window(pyglet.window.Window):
    def __init__(self):
        super(Game_Window,self).__init__(1024,768, "Симулятор муравейника")
        self.opengl_init()
        self.batch_01 = pyglet.graphics.Batch()
        self.layer_01 = pyglet.graphics.OrderedGroup(1)
        self.alive = 1

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
    
    def create_ant(self):
        new_ant = Ants(x=500, y=500, batch= self.batch_01, group= self.layer_01)
        new_ant.create()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LCTRL:
            self.create_ant()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == pyglet.window.mouse.LEFT:
            glTranslatef(-dx, -dy, 0)

game_window = Game_Window()
game_window.run()


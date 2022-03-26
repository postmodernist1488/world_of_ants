import pyglet

editor_window = pyglet.window.Window(1280, 720)
batch = pyglet.graphics.Batch()
grid = 1

if grid:
    white = pyglet.image.load('images/white_grid.png')
    black = pyglet.image.load('images/black_grid.png')
else:
    white = pyglet.image.load('images/white.png')
    black = pyglet.image.load('images/black.png')

class Square(pyglet.sprite.Sprite):
    def __init__(self, value, *args, **kwargs):
        super(Square, self).__init__(*args, **kwargs)
        self.value = value

class Map_Editor:
    def __init__(self):
        
        self.map_list = []
        self.scale = 2
        self.cell_size = 5 * self.scale
        self.colors = {white: 0, black: 10}
        
        self.offset_x = 0
        self.offset_y = 0
        editor_window.push_handlers(self)

    def edit(self, file_path):
        self.file_path = file_path
        with open(self.file_path, 'r') as map_file:
            for line in map_file:
                row = line.strip().split(', ')
                self.map_list.append(list(map(int, row)))

        self.squares = []
        for i in range(len(self.map_list)):
            temp = []
            for j in range(len(self.map_list[0])):
                img = white if self.map_list[i][j] else black
                value = 10 if self.map_list[i][j] else black
                sprite = Square(x=j*self.cell_size, y=i*self.cell_size, img=img, value=value, batch=batch)
                sprite.scale = self.scale
                temp.append(sprite)
            self.squares.append(temp)

    def save(self):
        with open(self.file_path, 'w') as map_file:
            for row in self.squares:
                line = []
                for square in row:
                    line.append(str(square.value))
                print(', '.join(line), file=map_file)
        print('Map saved successfully!')

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if modifiers == pyglet.window.key.MOD_CTRL:
            self.offset_x += dx
            self.offset_y += dy
            pyglet.gl.glTranslatef(dx, dy, 0)
        elif buttons & pyglet.window.mouse.LEFT and 0 <= x - self.offset_x < len(self.map_list[0]) * self.cell_size and 0 <= y - self.offset_y < (len(self.map_list)) * self.cell_size:
            square = self.squares[(y - self.offset_y) // self.cell_size][(x - self.offset_x) // self.cell_size]
            square.image = black
            square.value = 0

        elif buttons & pyglet.window.mouse.RIGHT and 0 <= x - self.offset_x < len(self.map_list[0]) * self.cell_size and 0 <= y + self.offset_y < len(self.map_list) * self.cell_size:
            square = self.squares[(y - self.offset_y) // self.cell_size][(x - self.offset_x) // self.cell_size]
            square.image = white
            square.value = 10

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.S and modifiers == pyglet.window.key.MOD_CTRL:
            self.save()


@editor_window.event 
def on_draw():
    editor_window.clear()
    batch.draw()





if __name__ == '__main__':
    map_editor = Map_Editor()
    map_editor.edit('map.txt')

    pyglet.app.run()
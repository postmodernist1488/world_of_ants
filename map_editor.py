import pyglet

editor_window = pyglet.window.Window(1280, 720)
batch = pyglet.graphics.Batch()
grid = 0

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
    def __init__(self, wall_value=0, space_value=1):
        self.wall_value = wall_value
        self.space_value = space_value
        self.map_list = []
        self.scale = 2
        self.cell_size = 5 * self.scale
        self.colors = {white: self.space_value, black: self.wall_value}
        
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
                if self.map_list[i][j] not in (self.wall_value, self.space_value):
                    raise ValueError("В файле разрешены только значения, указанные при создании объекта редактора.")
                img = white if self.map_list[i][j] == self.space_value else black
                value = self.space_value if self.map_list[i][j] == self.wall_value else self.wall_value
                sprite = Square(x=j*self.cell_size, y=(len(self.map_list) - 1 - i)*self.cell_size, img=img, value=value, batch=batch)
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
        print('Карта сохранена успешно!')

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == pyglet.window.mouse.MIDDLE:
            self.offset_x += dx
            self.offset_y += dy
            pyglet.gl.glTranslatef(dx, dy, 0)
        elif buttons & pyglet.window.mouse.LEFT and 0 <= x - self.offset_x < len(self.map_list[0]) * self.cell_size and 0 <= y - self.offset_y < (len(self.map_list)) * self.cell_size:
            square = self.squares[(len(self.map_list) * self.cell_size - y + self.offset_y - 1) // self.cell_size][(x - self.offset_x) // self.cell_size]
            square.image = black
            square.value = self.wall_value
        elif buttons & pyglet.window.mouse.RIGHT and 0 <= x - self.offset_x < len(self.map_list[0]) * self.cell_size and 0 <= y + self.offset_y < len(self.map_list) * self.cell_size:
            square = self.squares[(len(self.map_list) * self.cell_size - y + self.offset_y - 1) // self.cell_size][(x - self.offset_x) // self.cell_size]
            square.image = white
            square.value = self.space_value


    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.S:
            self.save()


@editor_window.event 
def on_draw():
    editor_window.clear()
    batch.draw()


if __name__ == '__main__':
    map_editor = Map_Editor(wall_value=0, space_value=1) # сюда указывать значения для стены (черный) и пространства (белый) - 
    map_editor.edit('map.txt')

    pyglet.app.run()
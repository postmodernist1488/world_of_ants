#400x200 (каждая координата 5*5) => 2000x1000 пикселей
#Муравьи ходят кратно квадратам карты
#10 - закрыто
#закрытые - изображение препятствия

from pyglet import shapes

class Game_Map():
    def __init__(self, scale:int, batch=None, group=None):
        self.count_x = 50
        self.count_y = 50
        self.map_list = []
        self.tile_list = []
        self.scale = scale
        self.batch = batch
        self.group = group

    def new_file(self):
        self.map_list = [[10] * self.count_x for _ in range(self.count_y)]
        with open('map.txt', 'w') as file_map:
            for i in range(len(self.map_list)):
                print(str(self.map_list[i])[1:-1], file=file_map)
        print('Новый файл успешно сгенерирован.')

    def load_file(self):
        with open('map.txt', 'r') as file_map:
            for line in file_map:
                row = line.rstrip('\n').split(', ')
                self.map_list.append(list(map(int, row)))
        self.map_list = list(reversed(self.map_list))
        
    def fill(self):
        self.load_file()
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == 1:
                    fb = Tile(x=j * self.scale, y=i * self.scale, scale=self.scale, batch=self.batch, group=self.group)
                    self.tile_list.append(fb)

class Tile(shapes.Rectangle):
    def __init__(self, x:int, y:int, scale:int, batch=None, group=None):
        super().__init__(x=x, y=y, width=scale, height=scale, color=(0, 0, 0), batch=batch, group=group)
        


if __name__ == '__main__':
    obj = Game_Map()
    #obj.new_file()
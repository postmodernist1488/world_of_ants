#400x200 (каждая координата 5*5) => 2000x1000 пикселей
#Муравьи ходят кратно квадратам карты
#0 - закрыто
#закрытые - изображение препятствия

from pyglet import shapes

class Game_Map():
    def __init__(self, scale:int=20, batch=None, group=None):
        self.count_x = 140
        self.count_y = 80
        self.map_list = []
        self.tile_list = []
        self.scale = scale
        self.batch = batch
        self.group = group

    def new_file(self, fill=0):
        self.map_list = [[fill] * self.count_x for _ in range(self.count_y)]
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
                    tl = Tile(x=j * self.scale, y=i * self.scale, scale=self.scale, batch=self.batch, group=self.group, track_type=1)
                else:
                    tl = Tile(x=j * self.scale, y=i * self.scale, scale=self.scale, batch=self.batch, group=self.group, track_type=0)
                
                self.tile_list.append(tl)

class Tile(shapes.Rectangle):

    track_list = [
    {4: (255, 255, 255)}, # empty tile
    {4: (0, 0, 0)}, # wall
    {0: (255, 255, 255), 1: (200, 255, 200), 2: (120, 255, 120), 3: (60, 255, 60), 4: (0, 255, 0)} # ant track tile
    ]

    def __init__(self, x:int, y:int, scale:int, track_type:int, batch=None, group=None):
        super().__init__(x=x, y=y, width=scale, height=scale, color=(0, 0, 0), batch=batch, group=group)
        self.new_track(track_type)

    def new_track(self, track_type: int):
        self.track_type = track_type
        self.track_power = 4
        self.color = self.track_list[self.track_type][self.track_power]     
    



if __name__ == '__main__':
    #create empty map
    Game_Map().new_file(0)
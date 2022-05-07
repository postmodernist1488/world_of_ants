class Game:
    def __init__(self):
        self.my_map = Map()
        self.ant_1 = Ant(self.my_map)
        self.ant_2 = Ant(self.my_map)
        self.ant_3 = Ant(self.my_map)
        self.ant_4 = Ant(self.my_map)
        
class Map:
    def __init__(self):
        self.x1 = []

class Ant():
    def __init__(self, map=None):
        self.map = map.x1
        self.map.append(13)
        print(self.map)

my_game = Game()

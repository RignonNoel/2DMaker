
class Map:

    map = []

    def __init__(self, file):
        self.file = file
        self.load_map()

    def load_map(self):
        # Init content of current map
        self.map = []

        # Load a new map
        f = open(self.file, mode='r')
        for line in f.readlines():
            line_map = []
            for char in line:
                if char != '\n':
                    line_map.append(char)
            self.map.append(line_map)

        print(self.map)

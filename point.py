from object import Object

class Point(Object):
    def __init__(self, name, coord):
        super().__init__(name, "point", coord)
    
    def draw(self, painter):
        a = 1
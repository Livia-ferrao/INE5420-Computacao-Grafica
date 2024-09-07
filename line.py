from object import Object

class Line(Object):
    def __init__(self, name, coord):
        super().__init__(name, "line", coord)
    
    def draw(self, painter):
        a = 1
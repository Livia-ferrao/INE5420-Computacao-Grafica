from object import Object

class Wireframe(Object):
    def __init__(self, name, coord):
        super().__init__(name, "wireframe", coord)

    def draw(self, painter):
        a = 1
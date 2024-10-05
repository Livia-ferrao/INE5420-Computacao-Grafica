from objects.object import Object
from PySide6.QtGui import QPen, QBrush, QColor, QPainterPath
from PySide6.QtCore import Qt
from tools.type import Type

class BerzierCurve(Object):
    def __init__(self, name, coord, color, qtd_points):
        super().__init__(name, Type.BERZIER_CURVE, coord, color)
        self.__qtd_points = qtd_points

    def getDrawingPoints(self):
        drawing_points = []

        for i in range(0, len(self.coord)-1, 3):
            p1 = self.coord[i]
            p2 = self.coord[i+1]
            p3 = self.coord[i+2]
            p4 = self.coord[i+3]

            x = self.__getBlendingFunctions(p1[0], p2[0], p3[0], p4[0])
            y = self.__getBlendingFunctions(p1[1], p2[1], p3[1], p4[1])

            passo = 1/(self.__qtd_points-1)
            t = 0
            for n in range(self.__qtd_points):
                drawing_points.append((x(t), y(t)))
                t += passo

        return drawing_points
    
    def __getBlendingFunctions(self, p1, p2, p3, p4):
        return lambda t: (p1*(-t**3 + 3*t**2 - 3*t + 1) + p2*(3*t**3 - 6*t**2 + 3*t)
                          + p3*(-3*t**3 + 3*t**2) + p4*t**3)

    def draw(self, coord_viewport, painter):
        a=1

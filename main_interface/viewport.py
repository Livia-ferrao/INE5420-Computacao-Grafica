from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt
from main_interface.configurations import Configurations

class Viewport():
    def __init__(self, window):
        self.__window = window

    # Desenhar borda vermelha da viewport
    def drawBorder(self, painter):
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(*Configurations.viewport())

    # Calcula as coordenadas de uma lista conforme a transformada de viewport para x e y
    def calcularCoordsViewport(self, coords):
        coord_viewport = []
        for coord in coords:
            x_viewport = self.__calcularXviewport(coord[0])
            y_viewport = self.__calcularYviewport(coord[1])
            coord_viewport.append((x_viewport, y_viewport))
        return coord_viewport

    # Cálculo do x da viewport conforme a transformada de viewport
    def __calcularXviewport(self, Xw):
        viewport_variance = Configurations.viewportXmax() - Configurations.viewportXmin()
        viewport__area_difference = Configurations.viewport()[0]
        xwmin = self.__window.xmin_scn
        xwmax = self.__window.xmax_scn
        return (viewport__area_difference + (((Xw - (xwmin))/(xwmax- (xwmin))) * viewport_variance))
    
    # Cálculo do y da viewport conforme a transformada de viewport
    def __calcularYviewport(self, Yw):
        viewport_variance = Configurations.viewportYmax() - Configurations.viewportYmin()
        viewport__area_difference = Configurations.viewport()[1]
        ywmin = self.__window.ymin_scn
        ywmax = self.__window.ymax_scn
        return (viewport__area_difference + ((1 - ((Yw - (ywmin))/ (ywmax - (ywmin)))) * viewport_variance))
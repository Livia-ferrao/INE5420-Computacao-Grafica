from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt
from main_interface.configurations import Configurations
import numpy as np


class Viewport():
    def __init__(self, window):
        self.__window = window

    # Desenhar borda vermelha da viewport
    def drawBorder(self, painter):
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(*Configurations.viewport())

   # Normalizar coordenadas
    def normalizeCoords(self, obj):
        transforming_matrix = self.__window.windowNormalize()
        
        # Coordenadas normalizadas de todos objetos da tela
        normalized_coords = []
        for x, y in obj.coord:
            transformed_coord = (np.dot(np.array([x, y, 1]), np.array(transforming_matrix))).tolist()
            normalized_coords.append(transformed_coord[:2])
        return normalized_coords

    # Cálculo do x da viewport conforme a transformada de viewport
    def calcularXviewport(self, Xw):
        viewport_variance = Configurations.viewportXmax() - Configurations.viewportXmin()
        viewport__area_difference = Configurations.viewport()[0]
        xwmin = self.__window.xmin_scn
        xwmax = self.__window.xmax_scn
        return (viewport__area_difference + (((Xw - (xwmin))/(xwmax- (xwmin))) * viewport_variance))
    
    # Cálculo do y da viewport conforme a transformada de viewport
    def calcularYviewport(self, Yw):
        viewport_variance = Configurations.viewportYmax() - Configurations.viewportYmin()
        viewport__area_difference = Configurations.viewport()[1]
        ywmin = self.__window.ymin_scn
        ywmax = self.__window.ymax_scn
        return (viewport__area_difference + ((1 - ((Yw - (ywmin))/ (ywmax - (ywmin)))) * viewport_variance))
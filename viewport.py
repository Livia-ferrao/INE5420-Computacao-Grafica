from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from configurations import Configurations
import numpy as np


class Viewport(QLabel):
    def __init__(self, parent, window):
        super().__init__(parent)
        self.__window = window
        self.setStyleSheet("border: none;")
        self.setGeometry(Configurations.viewport()[0],
                        Configurations.viewport()[1],
                        Configurations.viewport()[2],
                        Configurations.viewport()[3])
        # Pixmap para desenhar objetos
        self.__pix_map = QPixmap(Configurations.viewport()[2], Configurations.viewport()[3])
        self.__pix_map.fill(Qt.white)
        self.setPixmap(self.__pix_map)

    def drawObjects(self, obj_list):
        self.__pix_map.fill(Qt.white)
        painter = QPainter(self.__pix_map)

        # Desenha todos os objetos de obj_list
        for obj in obj_list:
            coord_viewport = []
            for coord in obj.coord:
                x_viewport = self.__calcularXviewport(coord[0])
                y_viewport = self.__calcularYviewport(coord[1])
                coord_viewport.append((x_viewport, y_viewport))
            obj.draw(coord_viewport, painter)
        self.setPixmap(self.__pix_map)

    # Cálculo do x da viewport conforme a transformada de viewport
    def __calcularXviewport(self, Xw):
        viewport_variance = Configurations.viewportXmax() - Configurations.viewportXmin()
        return (((Xw - self.__window.xw_min)/(self.__window.xw_max - self.__window.xw_min)) * viewport_variance)
    
    # Cálculo do y da viewport conforme a transformada de viewport
    def __calcularYviewport(self, Yw):
        viewport_variance = Configurations.viewportYmax() - Configurations.viewportYmin()
        return ((1 - ((Yw - self.__window.yw_min)/ (self.__window.yw_max - self.__window.yw_min))) * viewport_variance)
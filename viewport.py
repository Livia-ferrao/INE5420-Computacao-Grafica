from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from configurations import Configurations
import numpy as np


class Viewport():
    def __init__(self, parent, window):
        # super().__init__(parent)
        self.__window = window
        # self.setStyleSheet(
        #     "background-color: rgba(255, 255, 255, 0);\n"
        #     "border-color: rgb(255, 0, 0);\n"
        #     "border-width: 1.5px;\n"
        #     "border-style: solid;\n"
        # )
        # self.setGeometry(Configurations.viewport()[0],
        #                 Configurations.viewport()[1],
        #                 Configurations.viewport()[2],
        #                 Configurations.viewport()[3])
        # Pixmap para desenhar objetos
        # self.__pix_map = QPixmap(Configurations.viewport()[2], Configurations.viewport()[3])
        # self.__pix_map.fill(Qt.white)
        # self.setPixmap(self.__pix_map)

    # def drawObjects(self, obj_list):
    #     self.parent().pixmap().fill(Qt.white)
    #     painter = QPainter(self.parent().pixmap())
        
    #     # Normalizar as coordenadas
    #     normalized_coords = self.__normalizeCoords(obj_list)

    #     # Desenha todos os objetos de obj_list (e transforma pra Viewport)
    #     for idx, obj in enumerate(obj_list):
    #         coord_viewport = []
    #         for coord in normalized_coords[idx]:
    #             x_viewport = self.__calcularXviewport(coord[0])
    #             y_viewport = self.__calcularYviewport(coord[1])
    #             coord_viewport.append((x_viewport, y_viewport))
    #         obj.draw(coord_viewport, painter)
        
    #     self.parent().setPixmap(self.parent().pixmap())
    
   # Normalizar coordenadas
    def normalizeCoords(self, obj_list):
        transforming_matrix = self.__window.windowNormalize()
        
        # Coordenadas normalizadas de todos objetos da tela
        normalized_coords = []
        for obj in obj_list:
            obj_transformed_coords = []
            for x, y in obj.coord:
                transformed_coord = (np.dot(np.array([x, y, 1]), np.array(transforming_matrix))).tolist()
                obj_transformed_coords.append(transformed_coord[:2])
            normalized_coords.append(obj_transformed_coords)
        return normalized_coords

    # Cálculo do x da viewport conforme a transformada de viewport
    def calcularXviewport(self, Xw):
        viewport_variance = Configurations.viewportXmax() - Configurations.viewportXmin()
        viewport__area_difference = Configurations.viewport()[0]
        return (viewport__area_difference + (((Xw - (-1))/(1- (-1))) * viewport_variance))
    
    # Cálculo do y da viewport conforme a transformada de viewport
    def calcularYviewport(self, Yw):
        viewport_variance = Configurations.viewportYmax() - Configurations.viewportYmin()
        viewport__area_difference = Configurations.viewport()[1]
        return (viewport__area_difference + ((1 - ((Yw - (-1))/ (1 - (-1)))) * viewport_variance))
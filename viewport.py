from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from configurations import Configurations
import numpy as np


class Viewport(QLabel):
    def __init__(self, parent, window):
        super().__init__(parent)
        self.window = window
        self.setStyleSheet("border: none;")
        self.pix_map = QPixmap(Configurations.viewport()[2], Configurations.viewport()[3])
        self.pix_map.fill(Qt.white)
        self.setPixmap(self.pix_map)

    def draw_objects(self, obj_list):
        self.pix_map.fill(Qt.white)

        transforming_matrix = self.window.transforming_matrix
        painter = QPainter(self.pix_map)
        for obj in obj_list:
            transformed_coord = []
            print("coord", obj.coord)
            for x, y in obj.coord:
                coord_np = np.array([x, y, 1])
                matrix_np = np.array(transforming_matrix)
                print("matrix", matrix_np)
                dot_product = np.dot(coord_np, matrix_np)
                transformed_coord.append(dot_product.tolist()[0:2])
            print("transformed", transformed_coord)
            #if self.in_viewport(transformed_coord):

            coord_viewport = []
            for coord in transformed_coord:
                x_viewport = self.calcular_x_viewport(coord[0])
                y_viewport = self.calcular_y_viewport(coord[1])
                coord_viewport.append((x_viewport, y_viewport))

            obj.draw(coord_viewport, painter)
        self.setPixmap(self.pix_map)
    # def in_viewport(self, coord):
    #     if 

    def calcular_x_viewport(self, Xw):
        # Xw é uma coordenada X no sistema cartesiano da Window
        viewport_variance = Configurations.viewportXmax() - Configurations.viewportXmin()
        return (((Xw - self.window.xw_min)/(self.window.xw_max - self.window.xw_min)) * viewport_variance)
    
    def calcular_y_viewport(self, Yw):
        # Yw é uma coordenada Y no sistema cartesiano da Window
        viewport_variance = Configurations.viewportYmax() - Configurations.viewportYmin()
        return ((1 - ((Yw - self.window.yw_min)/ (self.window.yw_max - self.window.yw_min))) * viewport_variance)
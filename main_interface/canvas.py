from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from main_interface.configurations import Configurations
from tools.clipping import Clipping
from tools.type import Type, ClippingAlgorithm
from objects.line import Line

class Canvas(QLabel):
    def __init__(self, parent, viewport):
        super().__init__(parent)
        self.__viewport = viewport
        self.setStyleSheet("border: none;")
        self.setGeometry(*Configurations.canvas())

        # Pixmap para desenhar objetos
        self.__pix_map = QPixmap(Configurations.canvas()[2], Configurations.canvas()[3])
        self.__pix_map.fill(Qt.white)
        self.setPixmap(self.__pix_map)
    
    def drawObjects(self, obj_list, clipping_algorithm, window):
        self.__pix_map.fill(Qt.white)
        painter = QPainter(self.__pix_map)

        projection_matrix = window.getParallelProjectionMatrix()
        normalize_matrix = window.windowNormalize()

        for obj in obj_list:
            normalized = obj.projectAndNormalize(projection_matrix, normalize_matrix)
            
            if obj.tipo == Type.POINT or obj.tipo == Type.WIREFRAME:
                obj.draw(window, painter, self.__viewport, normalized)
            else:
                obj.draw(window, painter, self.__viewport, clipping_algorithm, normalized)
        
        self.__viewport.drawBorder(painter)
        
        self.setPixmap(self.__pix_map)

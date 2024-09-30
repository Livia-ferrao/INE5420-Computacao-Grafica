from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from main_interface.configurations import Configurations
from tools.clipping import Clipping

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

        # Desenha borda da viewport
        self.__viewport.drawBorder(painter)

        # Normalizar as coordenadas
        normalized_coords = self.__viewport.normalizeCoords(obj_list)

        # Desenha todos os objetos de obj_list (e transforma pra Viewport)
        for idx, obj in enumerate(obj_list):
            (draw, coords) = Clipping.clip(obj, normalized_coords[idx], window, clipping_algorithm)
            if draw:
                coord_viewport = []
                for coord in coords:
                    x_viewport = self.__viewport.calcularXviewport(coord[0])
                    y_viewport = self.__viewport.calcularYviewport(coord[1])
                    coord_viewport.append((x_viewport, y_viewport))
                obj.draw(coord_viewport, painter)
        
        self.setPixmap(self.__pix_map)

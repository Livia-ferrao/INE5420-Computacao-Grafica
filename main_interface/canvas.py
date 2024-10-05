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

        for obj in obj_list:
            if obj.tipo == Type.POINT:
                self.__drawPoint(obj, window, painter)
            elif obj.tipo == Type.LINE:
                self.__drawLine(obj, window, painter, clipping_algorithm)
            elif obj.tipo == Type.WIREFRAME:
                self.__drawWireframe(obj, window, painter)
            elif obj.tipo == Type.BERZIER_CURVE:
                self.__drawBerzierCurve(obj, window, painter, clipping_algorithm)
        
        self.__viewport.drawBorder(painter)
        
        self.setPixmap(self.__pix_map)
    
    def __drawPoint(self, obj, window, painter):
        # Normalizar as coordenadas
        normalized_coords = self.__viewport.normalizeCoords(obj)

        # Desenha todos os objetos de obj_list (e transforma pra Viewport)
        (draw, coords) = Clipping.pointClipping(normalized_coords, window)
        if draw:
            coord_viewport = []
            for coord in coords:
                x_viewport = self.__viewport.calcularXviewport(coord[0])
                y_viewport = self.__viewport.calcularYviewport(coord[1])
                coord_viewport.append((x_viewport, y_viewport))
            obj.draw(coord_viewport, painter)
    
    def __drawLine(self, obj, window, painter, clipping_algorithm):
        # Normalizar as coordenadas
        normalized_coords = self.__viewport.normalizeCoords(obj)

        # Desenha todos os objetos de obj_list (e transforma pra Viewport)
        if clipping_algorithm ==  ClippingAlgorithm.COHEN:
            (draw, coords) = Clipping.cohenSutherland(normalized_coords, window)
        else:
            (draw, coords) = Clipping.liangBarsky(normalized_coords, window)
        if draw:
            coord_viewport = []
            for coord in coords:
                x_viewport = self.__viewport.calcularXviewport(coord[0])
                y_viewport = self.__viewport.calcularYviewport(coord[1])
                coord_viewport.append((x_viewport, y_viewport))
            obj.draw(coord_viewport, painter)
    
    def __drawWireframe(self, obj, window, painter):
        # Normalizar as coordenadas
        normalized_coords = self.__viewport.normalizeCoords(obj)

        # Desenha todos os objetos de obj_list (e transforma pra Viewport)
        (draw, coords) = Clipping.sutherlandHodgeman(normalized_coords, window)
        if draw:
            coord_viewport = []
            for coord in coords:
                x_viewport = self.__viewport.calcularXviewport(coord[0])
                y_viewport = self.__viewport.calcularYviewport(coord[1])
                coord_viewport.append((x_viewport, y_viewport))
            obj.draw(coord_viewport, painter)
        
    def __drawBerzierCurve(self, obj, window, painter, clipping_algorithm):
        # Normalizar as coordenadas
        points = obj.getDrawingPoints()
        for i in range(len(points)-1):
            self.__drawLine(Line("", [points[i], points[i+1]], obj.color), window, painter, clipping_algorithm)
        

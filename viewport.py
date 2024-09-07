from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class Viewport(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    # def draw_objects(self, obj_list):
    #     painter = QPainter(self)
    #     painter.fillRect(self.rect(), Qt.white)
    #     for obj in obj_list:
    #         obj.draw(painter)
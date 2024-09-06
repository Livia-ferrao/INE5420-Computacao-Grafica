from PySide6.QtWidgets import QLabel
from PyQt5.QtGui import QPainter
from PyQt5.Qt import Qt

class Viewport(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

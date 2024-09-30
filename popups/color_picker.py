from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QSlider, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QImage, QColor, QPainter


class ColorPicker(QDialog):
    def __init__(self, color):
        super().__init__()
        self.setWindowTitle("Selecionar cor")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")

        # Valor do brilho inicializado no máximo
        self.__brightness = 1
        
        layout = QGridLayout(self)

        # Imagem do espectro de cores
        self.__color_spectrum = QLabel(self)
        self.__color_spectrum.setFixedSize(256, 256)
        self.__drawColorSpectrum(self.__color_spectrum.width(),
                                self.__color_spectrum.height())
        layout.addWidget(self.__color_spectrum, 0, 0, 1, 2)

        # Slider para controlar o brilho
        brightness_slider = QSlider(Qt.Horizontal)
        brightness_slider.setRange(0, 100)
        brightness_slider.setValue(100)
        brightness_slider.valueChanged.connect(self.__updateBrightness)
        layout.addWidget(brightness_slider, 1, 0, 1, 2)

        # Mostrar cor selecionada
        line_layout = QHBoxLayout()
        selected_color_label = QLabel("Cor selecionada:")
        line_layout.addWidget(selected_color_label)
        # Retângulo da cor selecionada
        self.__color_display = QLabel()
        self.__color_display.setFixedSize(80,20)
        line_layout.addWidget(self.__color_display)
        # Código da cor selecionada
        self.__color_code_label = QLabel()
        line_layout.addWidget(self.__color_code_label)
        # Cor selecionada inicialmente: cor passada na inicialização da classe
        self.__updateSelectedColor(color)
        layout.addLayout(line_layout, 2, 0, 1, 2)

        # Botões ok e cancelar
        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancelar")
        layout.addWidget(ok_button, 3, 1)
        layout.addWidget(cancel_button, 3, 0)
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        # Conectar clique do mouse
        self.__color_spectrum.mousePressEvent = self.__getColor

    # Desenha espectro de cores
    def __drawColorSpectrum(self, w, h):
        self.__spectrum_image = QImage(w, h, QImage.Format.Format_RGB32)
        painter = QPainter(self.__spectrum_image)

        # Calcula cor para cada ponto do espectro
        for x in range(w):
            for y in range(h):
                hue = x/w
                saturation = y/h
                color = QColor.fromHsvF(hue, saturation, self.__brightness)
                painter.setPen(color)
                painter.drawPoint(QPoint(x, y))
        painter.end()
        pixmap = QPixmap.fromImage(self.__spectrum_image)
        self.__color_spectrum.setPixmap(pixmap)

    # Coleta a cor clicada no espectro
    def __getColor(self, event):
        x = event.position().x()
        y = event.position().y()
        if 0 <= x < self.__color_spectrum.width() and 0 <= y < self.__color_spectrum.height():
            color = self.__color_spectrum.pixmap().toImage().pixelColor(int(x), int(y))
            self.__updateSelectedColor(color)

    # Atualiza a cor selecionada
    def __updateSelectedColor(self, color):
        self.__selected_color = color
        self.__color_display.setStyleSheet(f"background-color: {self.__selected_color.name()};")
        self.__color_code_label.setText(self.__selected_color.name())

    # Atualiza o brilho
    def __updateBrightness(self, value):
        self.__brightness = value/100
        self.__drawColorSpectrum(self.__color_spectrum.width(),
                                self.__color_spectrum.height())

    @property
    def selected_color(self):
        return self.__selected_color

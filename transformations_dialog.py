from PySide6.QtWidgets import QDialog, QTabWidget, QWidget
from PySide6.QtWidgets import QComboBox, QDialog, QLabel, QRadioButton, QGridLayout, QPushButton, QSpinBox, QScrollArea, QWidget, QDoubleSpinBox
from configurations import Configurations
from matrix_generator import MatrixGenerator
import numpy as np
from type import RotationType

class TransformationsDialog(QDialog):
    def __init__(self, selected_obj, window):
        super().__init__()
        self.__selected_obj = selected_obj
        self.__window = window
        # Desenha as abas
        self.__tab_widget = QTabWidget()
        self.__drawTranslationTab()
        self.__drawScalingTab()
        self.__drawRotationTab()

        self.__layout = QGridLayout(self)
        self.__layout.addWidget(self.__tab_widget, 0, 0)

        self.setFixedSize(400, 300)
        self.setWindowTitle("Transformações")
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
    
    # Desenha os botões para cada aba
    def __drawButtons(self, tab_layout, line, accept_function):
        ok_button = QPushButton("Aplicar")
        tab_layout.addWidget(ok_button, line, 1)
        cancel_button = QPushButton("Cancelar")
        tab_layout.addWidget(cancel_button, line, 0)
        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(accept_function)

    # Desenha aba de translação
    def __drawTranslationTab(self):
        self.__translation_tab = QWidget()
        
        # Inputs para dx e dy
        dx_label = QLabel("Deslocamento eixo x")
        self.__translation_dx = QSpinBox()
        self.__translation_dx.setRange(Configurations.min_coord(), Configurations.max_coord())
        dy_label = QLabel("Deslocamento eixo y")
        self.__translation_dy = QSpinBox()
        self.__translation_dy.setRange(Configurations.min_coord(), Configurations.max_coord())

        # Layout
        layout = QGridLayout(self.__translation_tab)
        layout.addWidget(dx_label, 0, 0)
        layout.addWidget(self.__translation_dx, 0, 1)
        layout.addWidget(dy_label, 1, 0)
        layout.addWidget(self.__translation_dy, 1, 1)

        # Desenha os botões da aba de translação
        self.__drawButtons(layout, 2, self.__translateObject)

        # Adiciona a aba de translação ao widget principal do dialog
        self.__tab_widget.addTab(self.__translation_tab, "Translação")
        
    # Desenha aba de escalonamento
    def __drawScalingTab(self):
        self.__scaling_tab = QWidget()
                
        # Input para escala
        scale_label = QLabel("Valor da escala:")
        self.__scale_input = QDoubleSpinBox()
        self.__scale_input.setRange(-100, 100)
        self.__scale_input.setSingleStep(0.1)
        
        # Layout
        layout = QGridLayout(self.__scaling_tab)
        layout.addWidget(scale_label, 0, 0)
        layout.addWidget(self.__scale_input, 0, 1)
        
        # Desenha os botões da aba de escalonamento
        self.__drawButtons(layout, 2, self.__scalingObject)

        # Adiciona a aba de escalonamento ao widget principal do dialog
        self.__tab_widget.addTab(self.__scaling_tab, "Escalonamento")
        
    # Desenha aba de rotação
    def __drawRotationTab(self):
        self.__rotation_tab = QWidget()
        
        # Escolha do ponto em torno do qual a rotação acontece
        rotation_label = QLabel("Ponto de rotação:")
        self.__rotation_type = QComboBox()
        self.__rotation_type.addItems([RotationType.OBJECT_CENTER.value,
                                     RotationType.WORLD_CENTER.value,
                                     RotationType.ARBITRARY_POINT.value])
        self.__rotation_type.currentIndexChanged.connect(self.__rotationTypeChanged)
        
        # Input do ângulo de rotação
        angle_label = QLabel("Ângulo de rotação (graus):")
        self.__angle_input = QSpinBox()
        self.__angle_input.setRange(-360, 360)
        self.__angle_input.setValue(0)  # Ângulo inicial
        
        # Labels e SpinBoxes para coordenadas do ponto arbitrário
        self.__rotation_dx_label = QLabel("Coordenada do ponto X:")
        self.__rotation_dx_input = QSpinBox()
        self.__rotation_dx_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        self.__rotation_dy_label = QLabel("Coordenada do ponto Y:")
        self.__rotation_dy_input = QSpinBox()
        self.__rotation_dy_input.setRange(Configurations.min_coord(), Configurations.max_coord())

        # Mostrar ou esconder labels e spinboxes do ponto arbitrário inicialmente de acordo com o tipo de rotação inicial
        self.__rotationTypeChanged()

        # Layout
        layout = QGridLayout(self.__rotation_tab)
        layout.addWidget(rotation_label, 0, 0)
        layout.addWidget(self.__rotation_type, 0, 1)
        layout.addWidget(angle_label, 1, 0)
        layout.addWidget(self.__angle_input, 1, 1)
        layout.addWidget(self.__rotation_dx_label, 2, 0)
        layout.addWidget(self.__rotation_dx_input, 2, 1)
        layout.addWidget(self.__rotation_dy_label, 3, 0)
        layout.addWidget(self.__rotation_dy_input, 3, 1)

        # Desenha os botões da aba de rotação
        self.__drawButtons(layout, 4, self.__rotateObject)
        
        # Adiciona a aba de rotação ao widget principal do dialog
        self.__tab_widget.addTab(self.__rotation_tab, "Rotação")
    
    # Mostra ou esconde labels e spinboxes do ponto arbitrário quando um tipo de rotação é selecionado
    def __rotationTypeChanged(self):
        current_text = self.__rotation_type.currentText()
        if current_text == RotationType.ARBITRARY_POINT.value:
            self.__rotation_dx_input.setEnabled(True)
            self.__rotation_dy_input.setEnabled(True)
            self.__rotation_dx_input.show()
            self.__rotation_dy_input.show()
            self.__rotation_dx_label.show()
            self.__rotation_dy_label.show()
        else:
            self.__rotation_dx_input.setEnabled(False)
            self.__rotation_dy_input.setEnabled(False)
            self.__rotation_dx_input.hide()
            self.__rotation_dy_input.hide()
            self.__rotation_dx_label.hide()
            self.__rotation_dy_label.hide()

    # Faz a translação do objeto
    def __translateObject(self):

        np_viewup = np.array(self.__window.view_up_vector)
        angle = np.degrees(np.arctan2(np_viewup[0], np_viewup[1]))

        rotation = MatrixGenerator.generateRotationMatrix(-angle)
        translating_matrix = MatrixGenerator.generateTranslationMatrix(self.__translation_dx.value(), self.__translation_dy.value())
        rotation_back = MatrixGenerator.generateRotationMatrix(angle)
        transforming_matrix = np.matmul(np.matmul(rotation, translating_matrix), rotation_back)
        self.__transformObject(transforming_matrix)
        self.accept()
        
    # Faz o escalonamento do objeto
    def __scalingObject(self):
        center_coord = self.__selected_obj.getCenter()

        translating = MatrixGenerator.generateTranslationMatrix(-center_coord[0], -center_coord[1])
        scaling = MatrixGenerator.generateScalingMatrix(self.__scale_input.value(), self.__scale_input.value())
        translating_back = MatrixGenerator.generateTranslationMatrix(center_coord[0], center_coord[1])

        transforming_matrix = np.matmul(np.matmul(translating, scaling), translating_back)
        self.__transformObject(transforming_matrix)
        self.accept()
    
    # Faz a rotação do objeto chamando a função adequada de rotação de acordo com o tipo de rotação escolhida
    def __rotateObject(self):
        rotation_type = self.__rotation_type.currentText()
        theta = self.__angle_input.value()
        
        if rotation_type == RotationType.OBJECT_CENTER.value:
            self.__rotateAroundObjectCenter(theta)
        elif rotation_type == RotationType.WORLD_CENTER.value:
            self.__rotateAroundWorldCenter(theta)
        elif rotation_type == RotationType.ARBITRARY_POINT.value:
            x = self.__rotation_dx_input.value()
            y = self.__rotation_dy_input.value()
            self.__rotateAroundArbitraryPoint(theta, (x, y))
        self.accept()
    
    # Faz a rotação do objeto em torno do seu centro
    def __rotateAroundObjectCenter(self, theta):
        center_coord = self.__selected_obj.getCenter()

        translating = MatrixGenerator.generateTranslationMatrix(-center_coord[0], -center_coord[1])
        rotation_matrix = MatrixGenerator.generateRotationMatrix(theta)
        translating_back = MatrixGenerator.generateTranslationMatrix(center_coord[0], center_coord[1])
        
        transforming_matrix = np.matmul(np.matmul(translating, rotation_matrix), translating_back)
        self.__transformObject(transforming_matrix)
    
    # Faz a rotação do objeto em torno do centro do mundo
    def __rotateAroundWorldCenter(self, theta):
        rotation_matrix = MatrixGenerator.generateRotationMatrix(theta)
        self.__transformObject(rotation_matrix)

    # Faz a rotação do objeto em torno de um ponto arbitrário
    def __rotateAroundArbitraryPoint(self, theta, coord):
        translating = MatrixGenerator.generateTranslationMatrix(-coord[0], -coord[1])
        rotation_matrix = MatrixGenerator.generateRotationMatrix(theta)
        translating_back = MatrixGenerator.generateTranslationMatrix(coord[0], coord[1])

        transforming_matrix = np.matmul(np.matmul(translating, rotation_matrix), translating_back)
        self.__transformObject(transforming_matrix)

    # Faz a transformação do objeto de acordo com uma matriz de transformação
    def __transformObject(self, matrix):
        new_coord = []
        for x, y in self.__selected_obj.coord:
            new = np.matmul(np.array([x, y, 1]), matrix).tolist()
            new_coord.append([new[0], new[1]])
        self.__selected_obj.coord = new_coord
        
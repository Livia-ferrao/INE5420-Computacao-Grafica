from PySide6.QtWidgets import QDialog, QTabWidget, QWidget
from PySide6.QtWidgets import QComboBox, QDialog, QLabel, QRadioButton, QGridLayout, QPushButton, QSpinBox, QScrollArea, QWidget, QDoubleSpinBox
from configurations import Configurations
from matrix_generator import MatrixGenerator
import numpy as np
from type import RotationType

class TransformationsDialog(QDialog):
    def __init__(self, selected_obj):
        super().__init__()
        self.__tab_widget = QTabWidget()
        self.__drawTranslationTab()
        self.__drawScalingTab()
        self.__drawRotationTab()

        self.__layout = QGridLayout(self)
        self.__layout.addWidget(self.__tab_widget, 0, 0)

        self.__selected_obj = selected_obj
        self.setFixedSize(400, 300)
        self.setWindowTitle("Transformações")
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
    
    def __drawButtons(self, tab_layout, line, accept_function):
        ok_button = QPushButton("Aplicar")
        tab_layout.addWidget(ok_button, line, 1)
        cancel_button = QPushButton("Cancelar")
        tab_layout.addWidget(cancel_button, line, 0)
        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(accept_function)

    def __drawTranslationTab(self):
        self.__translation_tab = QWidget()
        
        # layout
        layout = QGridLayout(self.__translation_tab)
        
        dx_label = QLabel("Deslocamento eixo x")
        self.__dx_input = QSpinBox()
        self.__dx_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        dy_label = QLabel("Deslocamento eixo y")
        self.__dy_input = QSpinBox()
        self.__dy_input.setRange(Configurations.min_coord(), Configurations.max_coord())

        layout.addWidget(dx_label, 0, 0)
        layout.addWidget(self.__dx_input, 0, 1)
        layout.addWidget(dy_label, 1, 0)
        layout.addWidget(self.__dy_input, 1, 1)

        self.__drawButtons(layout, 2, self.translateObject)
        self.__tab_widget.addTab(self.__translation_tab, "Translação")
        
    
    def __drawScalingTab(self):
        self.__scaling_tab = QWidget()
        
        # Layout
        layout = QGridLayout(self.__scaling_tab)
                
        # Desenhar escala
        scale_label = QLabel("Valor da escala:")
        self.scale_input = QDoubleSpinBox()
        self.scale_input.setRange(-100, 100)
        
        layout.addWidget(scale_label, 0, 0)
        layout.addWidget(self.scale_input, 0, 1)
        
        self.__drawButtons(layout, 2, self.scalingObject)
        self.__tab_widget.addTab(self.__scaling_tab, "Escalonamento")
        
    def __drawRotationTab(self):
        self.__rotation_tab = QWidget()
        
        # Layout
        layout = QGridLayout(self.__rotation_tab)
        
        rotacao_label = QLabel("Ponto de rotação:")
        self.rotacao_input = QComboBox()
        self.rotacao_input.addItems([RotationType.OBJECT_CENTER.value, RotationType.WORLD_CENTER.value, RotationType.ARBITRARY_POINT.value])
        self.rotacao_input.currentIndexChanged.connect(self.__combo_box_changed)
        
        # Label e SpinBox para o ângulo de rotação
        angulo_label = QLabel("Ângulo de rotação (graus):")
        self.angulo_input = QSpinBox()
        self.angulo_input.setRange(-360, 360)
        self.angulo_input.setValue(0)  # Ângulo inicial
        
        # Labels e SpinBoxes para coordenadas do ponto arbitrário
        self.dx_label = QLabel("Coordenada do ponto X:")
        self.dx_input = QSpinBox()
        self.dx_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        
        self.dy_label = QLabel("Coordenada do ponto Y:")
        self.dy_input = QSpinBox()
        self.dy_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        
        self.dz_label = QLabel("Coordenada do ponto Z:")
        self.dz_input = QSpinBox()
        self.dz_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        
        # Adicionando widgets ao layout
        layout.addWidget(rotacao_label, 0, 0)
        layout.addWidget(self.rotacao_input, 0, 1)
        layout.addWidget(angulo_label, 1, 0)
        layout.addWidget(self.angulo_input, 1, 1)
        
        # Adicionando widgets para coordenadas
        layout.addWidget(self.dx_label, 2, 0)
        layout.addWidget(self.dx_input, 2, 1)
        layout.addWidget(self.dy_label, 3, 0)
        layout.addWidget(self.dy_input, 3, 1)
        layout.addWidget(self.dz_label, 4, 0)
        layout.addWidget(self.dz_input, 4, 1)
        
        # Desenhar botão
        self.__drawButtons(layout, 5, self.rotationObject)
        
        # Adicionar a aba ao widget de abas
        self.__tab_widget.addTab(self.__rotation_tab, "Rotação")
    
    def __combo_box_changed(self):
        pass

    def translateObject(self):
        transforming_matrix = MatrixGenerator.generateTranslationMatrix(self.__dx_input.value(), self.__dy_input.value())
        self.__transformObject(transforming_matrix)
        self.accept()
        
    def scalingObject(self):
        center_coord = self.__selected_obj.get_center()
        translating = MatrixGenerator.generateTranslationMatrix(-center_coord[0], -center_coord[1])
        scaling = MatrixGenerator.generateScalingMatrix(self.scale_input.value(), self.scale_input.value())
        translating2 = MatrixGenerator.generateTranslationMatrix(center_coord[0], center_coord[1])
        transforming_matrix = np.matmul(np.matmul(translating, scaling), translating2)
        self.__transformObject(transforming_matrix)
        self.accept()
        
    def rotationObject(self):
        rotation_type = self.rotacao_input.currentText()
        theta = self.angulo_input.value()
        
        if rotation_type == RotationType.OBJECT_CENTER.value:
            self.rotateAroundObjectCenter(theta)
        elif rotation_type == RotationType.WORLD_CENTER.value:
            self.rotateAroundWorldCenter(theta)
        elif rotation_type == RotationType.ARBITRARY_POINT.value:
            x = self.dx_input.value()
            y = self.dy_input.value()
            z = self.dz_input.value()
            self.rotateAroundArbitraryPoint(theta, (x, y, z))
            
    def rotateAroundObjectCenter(self, theta):
        center_coord = self.__selected_obj.get_center()

        translating = MatrixGenerator.generateTranslationMatrix(-center_coord[0], -center_coord[1])
        rotation_matrix = MatrixGenerator.generateRotationMatrix(theta)
        translating_back = MatrixGenerator.generateTranslationMatrix(center_coord[0], center_coord[1])
        
        transforming_matrix = np.matmul(np.matmul(translating_back, rotation_matrix), translating)
        self.__transformObject(transforming_matrix)
        self.accept()
        
    def rotateAroundWorldCenter(self, theta):
        rotation_matrix = MatrixGenerator.generateRotationMatrix(theta)
        self.__transformObject(rotation_matrix)
        self.accept()

    def rotateAroundArbitraryPoint(self, theta, coord):
        translating = MatrixGenerator.generateTranslationMatrix(-coord[0], -coord[1])
        rotation_matrix = MatrixGenerator.generateRotationMatrix(theta)
        translating_back = MatrixGenerator.generateTranslationMatrix(coord[0], coord[1])

        transforming_matrix = np.matmul(np.matmul(translating_back, rotation_matrix), translating)
        self.__transformObject(transforming_matrix)
        self.accept()

    def __transformObject(self, matrix):
        new_coord = []
        print(self.__selected_obj.coord)
        for x, y in self.__selected_obj.coord:
            new = np.matmul(np.array([x, y, 1]), matrix).tolist()
            new_coord.append([new[0], new[1]])
        self.__selected_obj.coord = new_coord
        print(self.__selected_obj.coord)
        
from PySide6.QtWidgets import QDialog, QTabWidget, QWidget, QHBoxLayout
from PySide6.QtWidgets import QComboBox, QDialog, QLabel, QGridLayout, QPushButton, QSpinBox, QWidget, QDoubleSpinBox
from main_interface.configurations import Configurations
from tools.matrix_generator import MatrixGenerator
import numpy as np
from tools.type import RotationAxis

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

        self.setFixedSize(500, 350)
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
        self.__translation_dx = QDoubleSpinBox()
        self.__translation_dx.setRange(Configurations.min_coord(), Configurations.max_coord())
        dy_label = QLabel("Deslocamento eixo y")
        self.__translation_dy = QDoubleSpinBox()
        self.__translation_dy.setRange(Configurations.min_coord(), Configurations.max_coord())
        dz_label = QLabel("Deslocamento eixo z")
        self.__translation_dz = QDoubleSpinBox()
        self.__translation_dz.setRange(Configurations.min_coord(), Configurations.max_coord())

        # Layout
        layout = QGridLayout(self.__translation_tab)
        layout.addWidget(dx_label, 0, 0)
        layout.addWidget(self.__translation_dx, 0, 1)
        layout.addWidget(dy_label, 1, 0)
        layout.addWidget(self.__translation_dy, 1, 1)
        layout.addWidget(dz_label, 2, 0)
        layout.addWidget(self.__translation_dz, 2, 1)

        # Desenha os botões da aba de translação
        self.__drawButtons(layout, 3, self.__translateObject)

        # Adiciona a aba de translação ao widget principal do dialog
        self.__tab_widget.addTab(self.__translation_tab, "Translação")
        
    # Desenha aba de escalonamento
    def __drawScalingTab(self):
        self.__scaling_tab = QWidget()

        # Inputs para dx e dy
        sx_label = QLabel("Escala no eixo x:")
        self.__input_sx = QDoubleSpinBox()
        self.__input_sx.setRange(-100, 100)
        self.__input_sx.setSingleStep(0.1)
        self.__input_sx.setValue(1)
        sy_label = QLabel("Escala no eixo y:")
        self.__input_sy = QDoubleSpinBox()
        self.__input_sy.setRange(-100, 100)
        self.__input_sy.setSingleStep(0.1)
        self.__input_sy.setValue(1)
        sz_label = QLabel("Escala no eixo x:")
        self.__input_sz = QDoubleSpinBox()
        self.__input_sz.setRange(-100, 100)
        self.__input_sz.setSingleStep(0.1)
        self.__input_sz.setValue(1)

        # Layout
        layout = QGridLayout(self.__scaling_tab)
        layout.addWidget(sx_label, 0, 0)
        layout.addWidget(self.__input_sx, 0, 1)
        layout.addWidget(sy_label, 1, 0)
        layout.addWidget(self.__input_sy, 1, 1)
        layout.addWidget(sz_label, 2, 0)
        layout.addWidget(self.__input_sz, 2, 1)
        
        # Desenha os botões da aba de escalonamento
        self.__drawButtons(layout, 3, self.__scalingObject)

        # Adiciona a aba de escalonamento ao widget principal do dialog
        self.__tab_widget.addTab(self.__scaling_tab, "Escalonamento")
        
    # Desenha aba de rotação
    def __drawRotationTab(self):
        self.__rotation_tab = QWidget()
        
        # Input do ângulo de rotação
        angle_label = QLabel("Ângulo de rotação (graus):")
        self.__angle_input = QSpinBox()
        self.__angle_input.setRange(-360, 360)
        self.__angle_input.setValue(0)  # Ângulo inicial

        # Escolha do eixo de rotação
        axis_label = QLabel("Eixo de rotação:")
        self.__rotation_axis = QComboBox()
        self.__rotation_axis.addItems([RotationAxis.X.value,
                                     RotationAxis.Y.value,
                                     RotationAxis.Z.value,
                                     RotationAxis.ARBRITRARY.value])
        self.__rotation_axis.currentIndexChanged.connect(self.__rotationAxisChanged)

        # Labels e SpinBoxes para coordenadas do ponto do eixo arbitrárro
        self.__arbitrary_explanation = QLabel("O eixo arbitrário é o eixo entre o centro do objeto e o ponto:")
        self.__arbitrary_explanation.setFixedHeight(20) 
        self.__rotation_x_label = QLabel("x:")
        self.__rotation_x_input = QDoubleSpinBox()
        self.__rotation_x_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        self.__rotation_y_label = QLabel("y:")
        self.__rotation_y_input = QDoubleSpinBox()
        self.__rotation_y_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        self.__rotation_z_label = QLabel("z:")
        self.__rotation_z_input = QDoubleSpinBox()
        self.__rotation_z_input.setRange(Configurations.min_coord(), Configurations.max_coord())

        self.__rotationAxisChanged()

        # Layout
        layout = QGridLayout(self.__rotation_tab)
        layout.addWidget(angle_label, 0, 0)
        layout.addWidget(self.__angle_input, 0, 1)
        layout.addWidget(axis_label, 1, 0)
        layout.addWidget(self.__rotation_axis, 1, 1)
        layout.addWidget(self.__arbitrary_explanation, 2, 0, 1, 2)
        coords_hbox = QHBoxLayout()
        coords_hbox.addWidget(self.__rotation_x_label)
        coords_hbox.addWidget(self.__rotation_x_input)
        coords_hbox.addWidget(self.__rotation_y_label)
        coords_hbox.addWidget(self.__rotation_y_input)
        coords_hbox.addWidget(self.__rotation_z_label)
        coords_hbox.addWidget(self.__rotation_z_input)
        layout.addLayout(coords_hbox, 3, 0, 1, 2)
        
        # Desenha os botões da aba de rotação
        self.__drawButtons(layout, 4, self.__rotateObject)
        
        # Adiciona a aba de rotação ao widget principal do dialog
        self.__tab_widget.addTab(self.__rotation_tab, "Rotação")
    
    # Mostra ou esconde labels e spinboxes do ponto do eixo arbitrário quando um eixo é selecionado
    def __rotationAxisChanged(self):
        if self.__rotation_axis.currentText() == RotationAxis.ARBRITRARY.value:
            self.__rotation_x_input.setEnabled(True)
            self.__rotation_y_input.setEnabled(True)
            self.__rotation_z_input.setEnabled(True)
            self.__rotation_x_input.show()
            self.__rotation_y_input.show()
            self.__rotation_z_input.show()
            self.__rotation_x_label.show()
            self.__rotation_y_label.show()
            self.__rotation_z_label.show()
            self.__arbitrary_explanation.show()
        else:
            self.__rotation_x_input.setEnabled(False)
            self.__rotation_y_input.setEnabled(False)
            self.__rotation_z_input.setEnabled(False)
            self.__rotation_x_input.hide()
            self.__rotation_y_input.hide()
            self.__rotation_z_input.hide()
            self.__rotation_x_label.hide()
            self.__rotation_y_label.hide()
            self.__rotation_z_label.hide()
            self.__arbitrary_explanation.hide()

    # Faz a translação do objeto
    def __translateObject(self):
        self.__selected_obj.translate(self.__translation_dx.value(), self.__translation_dy.value(), self.__translation_dz.value())
        self.accept()
        
    # Faz o escalonamento do objeto
    def __scalingObject(self):
        self.__selected_obj.scale(self.__input_sx.value(), self.__input_sy.value(), self.__input_sz.value())
        self.accept()
    
    # Faz a rotação do objeto chamando a função adequada de rotação de acordo com o tipo de rotação escolhida
    def __rotateObject(self):
        rotation_axis = self.__rotation_axis.currentText()
        theta = self.__angle_input.value()

        if rotation_axis == RotationAxis.X.value:
            self.__selected_obj.rotateXAxis(theta)
        elif rotation_axis == RotationAxis.Y.value:
            self.__selected_obj.rotateYAxis(theta)
        elif rotation_axis == RotationAxis.Z.value:
            self.__selected_obj.rotateZAxis(theta)
        elif rotation_axis == RotationAxis.ARBRITRARY.value:
            point = (self.__rotation_x_input.value(), self.__rotation_y_input.value(), self.__rotation_z_input.value())
            self.__selected_obj.rotateArbitrary(theta, point)
        self.accept()
        
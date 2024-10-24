from PySide6.QtWidgets import QDialog, QTabWidget, QWidget, QHBoxLayout
from PySide6.QtWidgets import QComboBox, QDialog, QLabel, QGridLayout, QPushButton, QSpinBox, QWidget, QDoubleSpinBox
from main_interface.configurations import Configurations
from tools.matrix_generator import MatrixGenerator
import numpy as np
from tools.type import RotationType, RotationAxis

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
        self.__translation_dx = QSpinBox()
        self.__translation_dx.setRange(Configurations.min_coord(), Configurations.max_coord())
        dy_label = QLabel("Deslocamento eixo y")
        self.__translation_dy = QSpinBox()
        self.__translation_dy.setRange(Configurations.min_coord(), Configurations.max_coord())
        dz_label = QLabel("Deslocamento eixo z")
        self.__translation_dz = QSpinBox()
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
        
        # Escolha do ponto em torno do qual a rotação acontece
        rotation_label = QLabel("Rotação relativa ao:")
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
        self.__rotation_dx_label = QLabel("x:")
        self.__rotation_dx_input = QSpinBox()
        self.__rotation_dx_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        self.__rotation_dy_label = QLabel("y:")
        self.__rotation_dy_input = QSpinBox()
        self.__rotation_dy_input.setRange(Configurations.min_coord(), Configurations.max_coord())
        self.__rotation_dz_label = QLabel("z:")
        self.__rotation_dz_input = QSpinBox()
        self.__rotation_dz_input.setRange(Configurations.min_coord(), Configurations.max_coord())

        # Mostrar ou esconder labels e spinboxes do ponto arbitrário inicialmente de acordo com o tipo de rotação inicial
        self.__rotationTypeChanged()

        # Escolha do eixo de rotação
        axis_label = QLabel("Eixo de rotação:")
        self.__rotation_axis = QComboBox()
        self.__rotation_axis.addItems([RotationAxis.X.value,
                                     RotationAxis.Y.value,
                                     RotationAxis.Z.value,
                                     RotationAxis.ARBRITRARY.value])
        self.__rotation_axis.currentIndexChanged.connect(self.__rotationAxisChanged)

        self.__axis_labels = []
        self.__axis_inputs = []
        for i in ["x1:", "y1:", "z1:", "x2:", "y2:", "z2:"]:
            self.__axis_labels.append(QLabel(i))
            spin_box = QSpinBox()
            spin_box.setRange(Configurations.min_coord(), Configurations.max_coord())
            self.__axis_inputs.append(spin_box)

        self.__rotationAxisChanged()

        # Layout
        layout = QGridLayout(self.__rotation_tab)
        layout.addWidget(angle_label, 0, 0)
        layout.addWidget(self.__angle_input, 0, 1)
        layout.addWidget(rotation_label, 1, 0)
        layout.addWidget(self.__rotation_type, 1, 1)
        coords_hbox = QHBoxLayout()
        coords_hbox.addWidget(self.__rotation_dx_label)
        coords_hbox.addWidget(self.__rotation_dx_input)
        coords_hbox.addWidget(self.__rotation_dy_label)
        coords_hbox.addWidget(self.__rotation_dy_input)
        coords_hbox.addWidget(self.__rotation_dz_label)
        coords_hbox.addWidget(self.__rotation_dz_input)
        layout.addLayout(coords_hbox, 2, 0, 1, 2)
        layout.addWidget(axis_label, 3, 0)
        layout.addWidget(self.__rotation_axis, 3, 1)
        for i in range(2):
            hbox = QHBoxLayout()
            for j in range(3):
                hbox.addWidget(self.__axis_labels[i*3+j])
                hbox.addWidget(self.__axis_inputs[i*3+j])
            layout.addLayout(hbox, 4+i, 0, 1, 2)

        # Desenha os botões da aba de rotação
        self.__drawButtons(layout, 6, self.__rotateObject)
        
        # Adiciona a aba de rotação ao widget principal do dialog
        self.__tab_widget.addTab(self.__rotation_tab, "Rotação")
    
    # Mostra ou esconde labels e spinboxes do ponto arbitrário quando um tipo de rotação é selecionado
    def __rotationTypeChanged(self):
        current_text = self.__rotation_type.currentText()
        if current_text == RotationType.ARBITRARY_POINT.value:
            self.__rotation_dx_input.setEnabled(True)
            self.__rotation_dy_input.setEnabled(True)
            self.__rotation_dz_input.setEnabled(True)
            self.__rotation_dx_input.show()
            self.__rotation_dy_input.show()
            self.__rotation_dz_input.show()
            self.__rotation_dx_label.show()
            self.__rotation_dy_label.show()
            self.__rotation_dz_label.show()
        else:
            self.__rotation_dx_input.setEnabled(False)
            self.__rotation_dy_input.setEnabled(False)
            self.__rotation_dz_input.setEnabled(False)
            self.__rotation_dx_input.hide()
            self.__rotation_dy_input.hide()
            self.__rotation_dz_input.hide()
            self.__rotation_dx_label.hide()
            self.__rotation_dy_label.hide()
            self.__rotation_dz_label.hide()

    def __rotationAxisChanged(self):
        if self.__rotation_axis.currentText() == RotationAxis.ARBRITRARY.value:
            for i in range(6):
                self.__axis_labels[i].show()
                self.__axis_inputs[i].setEnabled(True)
                self.__axis_inputs[i].show()
        else:
            for i in range(6):
                self.__axis_labels[i].hide()
                self.__axis_inputs[i].setEnabled(False)
                self.__axis_inputs[i].hide()

    # Faz a translação do objeto
    def __translateObject(self):
        translating_matrix = MatrixGenerator.generateTranslationMatrix3D(self.__translation_dx.value(), self.__translation_dy.value(), self.__translation_dz.value())
        self.__transformObject(translating_matrix)
        self.accept()
        
    # Faz o escalonamento do objeto
    def __scalingObject(self):
        center_coord = self.__selected_obj.getCenter()

        translating = MatrixGenerator.generateTranslationMatrix3D(-center_coord[0], -center_coord[1], -center_coord[2])
        scaling = MatrixGenerator.generateScalingMatrix3D(self.__input_sx.value(), self.__input_sy.value(), self.__input_sz.value())
        translating_back = MatrixGenerator.generateTranslationMatrix3D(center_coord[0], center_coord[1], center_coord[2])

        transforming_matrix = np.matmul(np.matmul(translating, scaling), translating_back)
        self.__transformObject(transforming_matrix)
        self.accept()
        print(transforming_matrix)
    
    # Faz a rotação do objeto chamando a função adequada de rotação de acordo com o tipo de rotação escolhida
    def __rotateObject(self):
        rotation_axis = self.__rotation_axis.currentText()
        theta = self.__angle_input.value()
        rotation_point = self.__getRotationPoint()

        if rotation_axis == RotationAxis.X.value:
            self.__rotateX(theta, rotation_point)
        elif rotation_axis == RotationAxis.Y.value:
            self.__rotateY(theta, rotation_point)
        elif rotation_axis == RotationAxis.Z.value:
            self.__rotateZ(theta, rotation_point)
        elif rotation_axis == RotationAxis.ARBRITRARY.value:
            p1 = (self.__axis_inputs[0].value(), self.__axis_inputs[1].value(), self.__axis_inputs[2].value())
            p2 = (self.__axis_inputs[3].value(), self.__axis_inputs[4].value(), self.__axis_inputs[5].value())
            self.__rotateArbitrary(theta, rotation_point, p1, p2)
        self.accept()
    
    def __getRotationPoint(self):
        point = self.__rotation_type.currentText()
        if point == RotationType.OBJECT_CENTER.value:
            return self.__selected_obj.getCenter()
        elif point == RotationType.WORLD_CENTER.value:
            return (0, 0, 0)
        else:
            return (self.__rotation_dx_input.value(), self.__rotation_dy_input.value(), self.__rotation_dz_input.value())
    
    # Faz a rotação do objeto em torno do eixo x
    def __rotateX(self, theta, point):
        translating = MatrixGenerator.generateTranslationMatrix3D(-point[0], -point[1], -point[2])
        rotation_matrix = MatrixGenerator.generateRotationMatrix3D_X(theta)
        translating_back = MatrixGenerator.generateTranslationMatrix3D(point[0], point[1], point[2])
        
        transforming_matrix = np.matmul(np.matmul(translating, rotation_matrix), translating_back)
        self.__transformObject(transforming_matrix)
    
    # Faz a rotação do objeto em torno do eixo y
    def __rotateY(self, theta, point):
        translating = MatrixGenerator.generateTranslationMatrix3D(-point[0], -point[1], -point[2])
        rotation_matrix = MatrixGenerator.generateRotationMatrix3D_Y(theta)
        translating_back = MatrixGenerator.generateTranslationMatrix3D(point[0], point[1], point[2])
        
        transforming_matrix = np.matmul(np.matmul(translating, rotation_matrix), translating_back)
        self.__transformObject(transforming_matrix)

    # Faz a rotação do objeto em torno do eixo z
    def __rotateZ(self, theta, point):
        translating = MatrixGenerator.generateTranslationMatrix3D(-point[0], -point[1], -point[2])
        rotation_matrix = MatrixGenerator.generateRotationMatrix3D_Z(theta)
        translating_back = MatrixGenerator.generateTranslationMatrix3D(point[0], point[1], point[2])
        
        transforming_matrix = np.matmul(np.matmul(translating, rotation_matrix), translating_back)
        self.__transformObject(transforming_matrix)

    def __rotateArbitrary(self, theta, rotation_point, p1, p2):
        pass

    # Faz a transformação do objeto de acordo com uma matriz de transformação
    def __transformObject(self, matrix):
        new_coord = []
        for x, y, z in self.__selected_obj.coord:
            new = np.matmul(np.array([x, y, z, 1]), matrix).tolist()
            new_coord.append([new[0], new[1], new[2]])
        self.__selected_obj.coord = new_coord
        
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PySide6.QtWidgets import QMessageBox
#from edit_object import EditObject

from configurations import Configurations
from window import Window
from viewport import Viewport
from qtd_points import QtdPoints
from add_point import AddPoint
from add_line import AddLine
from add_wireframe import AddWireframe
from display_file import DisplayFile
from operationsMessage import OperationsMessage

class MainWindow(QtWidgets.QMainWindow):
    """
    This class inherits from PyQt5 and handles all configs to run the 
    main window of the application
    """
    def __init__(self):
        super().__init__()
        self.__display_file = DisplayFile()
        self.window = Window()
        self.setFixedSize(Configurations.window_X(), Configurations.window_Y())
        self.setWindowTitle('Window')
        self.setStyleSheet("background-color: rgb(212,208,200);")
        self.__draw_elements()

    def __build_frame(self, parent, x, y, w, h):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(x, y, w, h)
        frame.setStyleSheet("QFrame { border: 2px solid black; }")
    
        return frame

    def __draw_elements(self):
        # Frame de ferramentas (lateral esquerda)
        self.__tools_frame = self.__build_frame(self, Configurations.tool_frame()[0],
                                         Configurations.tool_frame()[1],
                                         Configurations.tool_frame()[2],
                                         Configurations.tool_frame()[3])
   
        # Frame de visualização (direita)
        self.__view_frame = self.__build_frame(self, Configurations.view_frame()[0],
                                         Configurations.view_frame()[1],
                                         Configurations.view_frame()[2],
                                         Configurations.view_frame()[3])

        # Frame da viewport
        self.__viewport = Viewport(self.__view_frame, self.window)
        self.__viewport.setGeometry(Configurations.viewport()[0],
                                Configurations.viewport()[1],
                                Configurations.viewport()[2],
                                Configurations.viewport()[3])
        self.viewport_label = QtWidgets.QLabel("Viewport", self.__view_frame)
        self.viewport_label.setGeometry(250, Configurations.viewport()[1] - 20, 140, 20)
        self.viewport_label.setStyleSheet("background-color: rgb(212,208,200); color: black; border: none;")

        # Label do frame de objetos
        self.__objects_label = QtWidgets.QLabel("Gerenciar objetos", self.__tools_frame)
        self.__objects_label.setGeometry(80, Configurations.objects_frame()[1] - 20, 140, 20)
        self.__objects_label.setStyleSheet("background-color: rgb(212,208,200); color: black; border: none;")

        # Frame de objetos
        self.__objects_frame = self.__build_frame(self.__tools_frame, Configurations.objects_frame()[0],
                                         Configurations.objects_frame()[1],
                                         Configurations.objects_frame()[2],
                                         Configurations.objects_frame()[3])
        self.__objects_frame.setStyleSheet("background-color: rgb(165,165,165);")

        # Label do frame de controle da window
        self.__objects_label = QtWidgets.QLabel("Controle da window", self.__tools_frame)
        self.__objects_label.setGeometry(80, Configurations.control_frame()[1] - 20, 140, 20)
        self.__objects_label.setStyleSheet("background-color: rgb(212,208,200); color: black; border: none;")

        # Frame de controle da window
        self.__control_frame = self.__build_frame(self.__tools_frame, Configurations.control_frame()[0],
                                         Configurations.control_frame()[1],
                                         Configurations.control_frame()[2],
                                         Configurations.control_frame()[3])
        self.__control_frame.setStyleSheet("background-color: rgb(165,165,165);")
        
        # Botões de controle da window
        layout_control = QtWidgets.QGridLayout(self.__control_frame)

        self.__btnUp = QtWidgets.QPushButton(self.__control_frame)
        self.__btnDown = QtWidgets.QPushButton(self.__control_frame)
        self.__btnLeft = QtWidgets.QPushButton(self.__control_frame)
        self.__btnRight = QtWidgets.QPushButton(self.__control_frame)
        self.__btnZoomIn = QtWidgets.QPushButton(self.__control_frame)
        self.__btnZoomOut = QtWidgets.QPushButton(self.__control_frame)

        self.__btnRight.setIcon(QtGui.QIcon("icons/right-arrow.png"))
        self.__btnDown.setIcon(QtGui.QIcon("icons/down-arrow.png"))
        self.__btnLeft.setIcon(QtGui.QIcon("icons/left-arrow.png"))
        self.__btnUp.setIcon(QtGui.QIcon("icons/up-arrow.png"))
        self.__btnZoomIn.setIcon(QtGui.QIcon("icons/zoom-in.png"))
        self.__btnZoomOut.setIcon(QtGui.QIcon("icons/zoom-out.png"))

        layout_control.addWidget(self.__btnUp, 1, 2)
        layout_control.addWidget(self.__btnLeft, 2, 1)
        layout_control.addWidget(self.__btnRight, 2, 3)
        layout_control.addWidget(self.__btnDown, 3, 2)
        layout_control.addWidget(self.__btnZoomIn, 1, 0)
        layout_control.addWidget(self.__btnZoomOut, 3, 0)
 
        self.__btnZoomOut.clicked.connect(self.__zoom_out)
        self.__btnZoomIn.clicked.connect(self.__zoom_in)
        self.__btnUp.clicked.connect(self.__move_up)
        self.__btnDown.clicked.connect(self.__move_down)
        self.__btnLeft.clicked.connect(self.__move_left)
        self.__btnRight.clicked.connect(self.__move_right)

        self.__btnZoomOut.setStyleSheet("background-color: rgb(212,208,200);")
        self.__btnZoomIn.setStyleSheet("background-color: rgb(212,208,200);")
        self.__btnUp.setStyleSheet("background-color: rgb(212,208,200);")
        self.__btnDown.setStyleSheet("background-color: rgb(212,208,200);")
        self.__btnLeft.setStyleSheet("background-color: rgb(212,208,200);")
        self.__btnRight.setStyleSheet("background-color: rgb(212,208,200);")

        self.__control_scale = QtWidgets.QDoubleSpinBox()
        self.__control_scale.setValue(10.00)
        self.__control_scale.setMinimum(0.01)
        self.__control_scale.setMaximum(99.99)
        self.__control_scale.setSingleStep(1)
        self.__control_scale.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.__scale_label = QtWidgets.QLabel("%")
        self.__scale_label.setStyleSheet("color: black; border: none;")
        layout_control.addWidget(self.__control_scale, 0, 0)
        layout_control.addWidget(self.__scale_label, 0, 1)

        # Botões no frame de objetos
        self.__combo_box = QtWidgets.QComboBox(self.__objects_frame)
        self.__combo_box.setGeometry(165, 30, 100, 30)
        self.__combo_box.addItems(["Ponto", "Reta", "Polígono"])
        self.__combo_box.setStyleSheet("background-color: rgb(212,208,200); color: black")
        
        self.__add_button = QtWidgets.QPushButton('Adicionar', self.__objects_frame)
        self.__add_button.setGeometry(165, 80, 100, 30)
        self.__add_button.clicked.connect(self.add_object)
        self.__add_button.setStyleSheet("background-color: rgb(212,208,200); color: black")

        self.__add_button = QtWidgets.QPushButton('Operações', self.__objects_frame)
        self.__add_button.setGeometry(165, 120, 100, 30)
        self.__add_button.clicked.connect(self.choose_operation)
        self.__add_button.setStyleSheet("background-color: rgb(212,208,200); color: black")

        # Lista de objetos
        self.__object_list = QtWidgets.QListWidget(self.__objects_frame)
        self.__object_list.setGeometry(10, 10, 140, 145)
        self.__object_list.setStyleSheet("background-color: rgb(240,240,240); color: black; border: 1px solid black")


    def add_object(self):
        selected_option = self.__combo_box.currentText()
        if selected_option == "Ponto":
            add_dialog = AddPoint(self.__display_file.get_names())
        elif selected_option == "Reta":
            add_dialog = AddLine(self.__display_file.get_names())
        elif selected_option == "Polígono":
            qtd_dialog = QtdPoints()
            if qtd_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                add_dialog = AddWireframe(self.__display_file.get_names(), qtd_dialog.qtd_input.value(), qtd_dialog.preencher.isChecked())
        if add_dialog:
            if add_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                obj = add_dialog.create()
                self.__display_file.add_object(obj)
                self.__object_list.addItem(str(obj.name))
                self.__viewport.draw_objects(self.__display_file.objects_list)

    def choose_operation(self):
        index_selected_obj = self.__object_list.currentRow()
        if index_selected_obj != -1:
            operations_message = OperationsMessage()
            op = operations_message.exec()
            
            if op == QtWidgets.QMessageBox.Open:
                self.delete_object(index_selected_obj)
            if op == QtWidgets.QMessageBox.Ok:
                 self.edit_object(index_selected_obj)
            else:
                pass
        else:
            message = QMessageBox()
            message.setWindowTitle("Aviso")
            message.setText("Selecione um objeto para realizar uma operação")
            message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
            message.setFixedSize(400, 200)
            message.exec()
    
    def delete_object(self, index_selected_obj):
        self.__object_list.takeItem(index_selected_obj)
        self.__display_file.remove_object(index_selected_obj)
        self.__viewport.draw_objects(self.__display_file.objects_list)

    def edit_object(self, index_selected_obj):
        selected_item = self.__object_list.item(index_selected_obj)
        if selected_item:
            print(selected_item)
            selected_object = selected_item.data(QtCore.Qt.UserRole)
            print(selected_object)
            if selected_object:
                print(selected_object)
            #     edit_window = EditObject(existing_object=selected_object)               
            #     if edit_window.exec() == QtWidgets.QDialog.Accepted:
            #         updated_object = edit_window.existing_object
            #         selected_item.setText(updated_object.name) 
            #         self.__display_file.update_object(index_selected_obj, updated_object)
            #         self.__viewport.draw_objects(self.__display_file.objects_list)

    def __move_left(self):
        self.window.move_left(self.__control_scale.value())
        self.__viewport.draw_objects(self.__display_file.objects_list)
    
    def __move_right(self):
        self.window.move_right(self.__control_scale.value())
        self.__viewport.draw_objects(self.__display_file.objects_list)

    def __move_up(self):
        self.window.move_up(self.__control_scale.value())
        self.__viewport.draw_objects(self.__display_file.objects_list)
    
    def __move_down(self):
        self.window.move_down(self.__control_scale.value())
        self.__viewport.draw_objects(self.__display_file.objects_list)
    
    def __zoom_in(self):
        self.window.zoom_in(self.__control_scale.value())
        self.__viewport.draw_objects(self.__display_file.objects_list)
    
    def __zoom_out(self):
        self.window.zoom_out(self.__control_scale.value())
        self.__viewport.draw_objects(self.__display_file.objects_list)
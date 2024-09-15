from PySide6.QtWidgets import QDialog, QTabWidget, QWidget

class TransformationsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.__tab_widget = QTabWidget()
        self.__drawTranslationTab()
        self.__drawScalingTab()
        self.__drawRotationTab()
    
    def __drawTranslationTab(self):
        self.__tranlation_tab = QWidget()
        pass
    
    def __drawScalingTab(self):
        pass

    def __drawRotationTab(self):
        pass

# CÓDIGO CHATGPT PARA SE BASEAR
# class MyDialog(QDialog):
#     def __init__(self):
#         super().__init__()
        
#         # Crie o QTabWidget
#         self.tab_widget = QTabWidget()
        
#         # Crie o conteúdo das abas
#         self.tab1 = QWidget()
#         self.tab2 = QWidget()
#         self.tab3 = QWidget()
        
#         # Adicione o conteúdo às abas
#         self.tab1_layout = QVBoxLayout()
#         self.tab1_layout.addWidget(QLabel("Conteúdo da Aba 1"))
#         self.tab1.setLayout(self.tab1_layout)
        
#         self.tab2_layout = QVBoxLayout()
#         self.tab2_layout.addWidget(QLabel("Conteúdo da Aba 2"))
#         self.tab2.setLayout(self.tab2_layout)
        
#         self.tab3_layout = QVBoxLayout()
#         self.tab3_layout.addWidget(QLabel("Conteúdo da Aba 3"))
#         self.tab3.setLayout(self.tab3_layout)
        
#         # Adicione as abas ao QTabWidget
#         self.tab_widget.addTab(self.tab1, "Aba 1")
#         self.tab_widget.addTab(self.tab2, "Aba 2")
#         self.tab_widget.addTab(self.tab3, "Aba 3")
        
#         # Crie um layout para o QDialog e adicione o QTabWidget
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.tab_widget)
#         self.setLayout(self.layout)

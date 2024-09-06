# import sys
# from PyQt5.QtWidgets import QApplication
# from main_window import MainWindow

# class Application(QApplication):
#     """
#     This class inherits from PyQt5 and handles all configs to run the 
#     application
#     """
#     def __init__(self):
#         super(Application, self).__init__(sys.argv)
#         # self.__display_file = DisplayFile()
#         # self.__g_object_handler = GObjectHandler(self.__display_file)
#         self.__main_window = MainWindow()

#     def run(self) -> None:
#         self.__main_window.show()
#         sys.exit(self.exec_())

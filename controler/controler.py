import sys
from PyQt5.QtWidgets import QApplication
from resources.main_window import MainWindow

class MainPresetator:
    def iniciar(self):
        app = QApplication(sys.argv)
        _win = MainWindow()
        _win.showMaximized() # to make the application has the maximum size when executed, while still allowing the user to resize it
        app.exec()
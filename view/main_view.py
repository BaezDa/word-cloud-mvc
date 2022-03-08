from PyQt5.QtWidgets import QMainWindow, QFileDialog

from view.main_view_generated_ui import Ui_MainWindow
from view.mpl_canvas_view import MplCanvas

class MainView(QMainWindow, Ui_MainWindow):
   """Clase complementaria para extender las funcionalidades
   de la vista.

   Args:
       QMainWindow (_type_): _description_
       Ui_MainWindow (_type_): _description_
   """
   def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.file_dialog = QFileDialog(self)
        self.mpl_canvas_cloud = MplCanvas(self, width=6, height=4, dpi=100)
        self.mpl_canvas_hist = MplCanvas(self, width=6, height=4, dpi=100)
        self.tabWidget.setCurrentIndex(0)
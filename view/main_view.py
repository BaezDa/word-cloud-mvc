from PyQt5.QtWidgets import QMainWindow, QFileDialog

from view.main_view_generated_ui import Ui_MainWindow
from view.mpl_canvas_view import MplCanvas

class MainView(QMainWindow, Ui_MainWindow):
   def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.file_dialog = QFileDialog(self)
        self.mpl_canvas = MplCanvas(self, width=5, height=4, dpi=100)
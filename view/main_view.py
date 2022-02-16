from PyQt5.QtWidgets import QMainWindow

from view.main_view_ui import Ui_Form

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_Form()
        self._ui.setupUi(self)
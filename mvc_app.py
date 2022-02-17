import sys
from PyQt5.QtWidgets import QApplication
from model.list_model import ListModel
from controller.main_controller import MainController
from view.main_view import MainView


if __name__ == "__main__":
    app = QApplication([])
    model = ListModel()
    main_view = MainView()
    main_ctrl = MainController(main_view, model )
    main_view.show()
    app.exec_()

import sys
from PyQt5.QtWidgets import QApplication
from model.list_model import ListModel
from controller.main_controller import MainController
from view.main_view import MainView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # Connect everything together
        self.model = ListModel()
        self.main_view = MainView()
        self.main_ctrl = MainController(self.main_view._ui, self.model )
        self.main_view.show()


# if __name__ == '__main__':
#     app = App(sys.argv)
#     sys.exit(app.exec_())

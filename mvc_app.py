import sys
from PyQt5.QtWidgets import QApplication
from model.ListModel import ListModel
from controller.MainController import MainController
from view.main_view import MainView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # Connect everything together
        self.model = Model()
        self.main_ctrl = MainController(self.model,  )
        self.main_view = MainView(self.model, self.main_ctrl)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
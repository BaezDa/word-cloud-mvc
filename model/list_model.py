from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class ListModel(QtCore.QAbstractListModel):
    
    def __init__(self, *args, todos=None, **kwargs):
        super(ListModel, self).__init__(*args, **kwargs)
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the data structure.
            status, text = self.todos[index.row()]
            # Return the todo text only.
            return text

    def rowCount(self, index):
        return len(self.todos)
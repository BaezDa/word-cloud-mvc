from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class ListModel(QtCore.QAbstractListModel):
    """Modelo lista
    
    Esta clase representa a lista de cosas que se agreguen en las palabras clave,
    herada de QAbstractListModel, por lo que se sobreescriben los métodos de acuerdo
    a las necesidades.
    Args:
        QtCore (_type_): _description_
    """
    def __init__(self, *args, todos=None, **kwargs):
        super(ListModel, self).__init__(*args, **kwargs)
        self.todos = todos or []

    def data(self, index, role):
        """Retorna un elemento de la lista en base
        a su index y role.
        
        
        Args:
            index (_type_): _description_
            role (_type_): _description_

        Returns:
            _type_: _description_
        """
        if role == Qt.DisplayRole:
            text = self.todos[index.row()]
            return text
        
    def get_data(self):
        return self.todos

    
    def rowCount(self, index):
        return len(self.todos)
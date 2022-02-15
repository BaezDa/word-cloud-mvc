import os
import sys
from os.path import dirname, realpath, join
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUiType

import pandas as pd



scriptDir = dirname(realpath(__file__))
From_Main, _ = loadUiType(join(dirname(__file__), "window.ui"))


class MainWindow(QWidget, From_Main):
    def __init__(self):
        super(MainWindow, self).__init__()
        QWidget.__init__(self)
        self.setupUi(self)
        self.model = ListModel()
        self.listView.setModel(self.model)

        self.spinBox.setValue(10)
        self.ButtonOpen.clicked.connect(self.OpenFile)
        self.BtnDescribe.clicked.connect(self.dataHead)
        self.BtnAceptar.clicked.connect(self.add)

    def OpenFile(self):
        try:
            path = QFileDialog.getOpenFileName(
                self, 'Abrir CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            self.all_data = pd.read_csv(path)
            print(path)
        except:
            print(path)

    def dataHead(self):
        numColomn = self.spinBox.value()
        if numColomn == 0:
            NumRows = len(self.all_data.index)
        else:
            NumRows = numColomn
        self.tableWidget.setColumnCount(len(self.all_data.columns))
        self.tableWidget.setRowCount(NumRows)
        self.tableWidget.setHorizontalHeaderLabels(self.all_data.columns)

        for i in range(NumRows):
            for j in range(len(self.all_data.columns)):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(self.all_data.iat[i, j])))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def add(self):
        text = self.lineEdit.text()
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.
            self.model.layoutChanged.emit()
            # Empty the input
            self.todoEdit.setText("")


app = QApplication(sys.argv)
sheet = MainWindow()
sheet.show()
sys.exit(app.exec_())

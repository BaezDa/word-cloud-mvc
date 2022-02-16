import os
import sys
from os.path import dirname, realpath
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
# from PyQt5.uic import loadUiType

import pandas as pd



scriptDir = dirname(realpath(__file__))
#From_Main, _ = loadUiType(join(dirname(__file__), "window.ui"))


class MainController():
    
    def __init__(self, view, model):
        
        self.model = model
        self.view = view
        
        self.view.listView.setModel(self.model)
        self.view.spinBox.setValue(10)
        
        #
        self.view.ButtonOpen.clicked.connect(self.OpenFile)
        self.view.BtnDescribe.clicked.connect(self.dataHead)
        self.view.BtnAceptar.clicked.connect(self.add)

        # self.view.btn.clicked.connect(self.onBtnMainClicked)

        # self.view.show()

      

    def OpenFile(self):
        try:
            path = QFileDialog.getOpenFileName(
                self, 'Abrir CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            self.all_data = pd.read_csv(path)
            print(path)
        except:
            print(path)

    def dataHead(self):
        numColomn = self.view.spinBox.value()
        if numColomn == 0:
            NumRows = len(self.all_data.index)
        else:
            NumRows = numColomn
        self.view.tableWidget.setColumnCount(len(self.all_data.columns))
        self.view.tableWidget.setRowCount(NumRows)
        self.view.tableWidget.setHorizontalHeaderLabels(self.all_data.columns)

        for i in range(NumRows):
            for j in range(len(self.all_data.columns)):
                self.view.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(self.all_data.iat[i, j])))

        self.view.tableWidget.resizeColumnsToContents()
        self.view.tableWidget.resizeRowsToContents()

    def add(self):
        text = self.view.lineEdit.text()
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.
            self.model.layoutChanged.emit()
            # Empty the input
            self.view.lineEdit.setText("")


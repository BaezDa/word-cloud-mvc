import os
import sys
from os.path import dirname, realpath
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
# from PyQt5.uic import loadUiType
from pathlib import Path



import pandas as pd



scriptDir = dirname(realpath(__file__))

class MainController():
    
    def __init__(self, view, model):
        
        self.model = model
        self.view = view
        
        self.view.listView.setModel(self.model)
        self.view.spinBox.setValue(10)

        #Canvas
        self.view.mpl_canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        
        #Primer Tab
        self.view.ButtonOpen.clicked.connect(self.open_file)
        self.view.BtnDescribe.clicked.connect(self.data_head)
        self.view.BtnAceptar.clicked.connect(self.add)
        self.view.BtnReducir.clicked.connect(self.reduce_db)

        # self.view.btn.clicked.connect(self.onBtnMainClicked)

        self.path = ""
        
        #Segundo Tab
        self.view.BtnCloud.clicked.connect(self.show_image)

    def open_file(self):
        try:
            path = self.view.file_dialog.getOpenFileName(self.view, 'Abrir CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            self.all_data = pd.read_csv(path)
            print(path)
        except:
            print(path)

    def data_head(self):
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
            self.model.todos.append(text)
            # Trigger refresh.
            self.model.layoutChanged.emit()
            # Empty the input
            self.view.lineEdit.setText("")
    
    def reduce_db(self):
        actors = self.model.get_data()
        print(actors)
        db_reducida = self.all_data[self.all_data['Texto'].str.contains('|'.join(actors))]
       
        filepath = Path('C:/Users/Baez/Documents/UAC/8vo semestre/Topicos de lenguajes de programación/Primer parcial/Programa 1 Python/word-cloud-mvc/out.csv')  
        db_reducida.to_csv(filepath) 

    def show_image(self):
        self.view.mpl_canvas.setParent(self.view.frameNube)
        self.view.mpl_canvas.show()
        

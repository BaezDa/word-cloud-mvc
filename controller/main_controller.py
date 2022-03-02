import os
import sys
from os.path import dirname, realpath
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from pathlib import Path

from model.word_cloud import WordCloudI

import pandas as pd



scriptDir = dirname(realpath(__file__))

class MainController():
    
    def __init__(self, view, model):
        
        self.model = model
        self.view = view
        
        self.path = ""
        
        
        #Valores iniciales del modelo y spinbox        
        self.view.listView.setModel(self.model)
        self.view.spinBox.setValue(10)

       
        
        self.view.ButtonOpen.clicked.connect(self.open_file)
        
        #Primer Tab
        self.view.BtnDescribe.clicked.connect(self.data_head)
        self.view.BtnAceptar.clicked.connect(self.add)
        self.view.BtnReducir.clicked.connect(self.reduce_db)


        
        #Segundo Tab
        self.view.BtnCloud.clicked.connect(self.show_cloud)
        
        
        #Tercer Tab
        self.view.BtnGraficar.clicked.connect(self.show_hist)

    def open_file(self):
        """Abre el archivo CSV.
        
        Despliega una ventana donde se escoge el archivo CSV.
        
        """
        try:
            path = self.view.file_dialog.getOpenFileName(self.view, 'Abrir CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            self.all_data = pd.read_csv(path)
            print(path)
        except:
            print(path)
            
    def save_file(self):
        """Abre el archivo CSV.
        
        Despliega una ventana donde se escoge el archivo CSV.
        
        """
        try:
            path = self.view.file_dialog.getSaveFileName(self.view, 'Guardar CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            # self.all_data = pd.read_csv(path)
            print(path)
            return path
        except:
            print(path)

    def data_head(self):
        """Carga los datos del archivos CSV en TableWidget.
        
        Recorre el archivo CSV para asignarlos en las propiedades
        de un TableWidget.
        
        """
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
        """Agrega elementos a lista del modelo.
        
        Actualiza el modelo cada vez que se agrega un elemento,
        por lo que require de un emit() para reflejar los cambios
        del modelo en la interfaz.
        
        """
        text = self.view.lineEdit.text()
        if text:  # No se agregan cadenas vacias.
            self.model.todos.append(text)
            self.model.layoutChanged.emit()
            self.view.lineEdit.setText("")
    
    def reduce_db(self):
        """Crea una base de datos reducida.
        
        Obtiene las palabras clave del modelo para filtrar los datos,
        esto con la finalidad de crear el archivo csv reducido.
        """
        actors = self.model.get_data()
        print(actors)
        db_reducida = self.all_data[self.all_data['Texto'].str.contains('|'.join(actors))]
        
        filepath = Path(self.save_file())  
        db_reducida.to_csv(filepath) 

    def show_cloud(self):
        """Muestra la nube de palabras.
        
        Agrega la imagen generada de la nube de palabras a su contenedor canvas
        correspondiente.
        """
        text =  " ".join(review for review in self.all_data['Texto'])
        self.view.mpl_canvas_cloud.axes.imshow(WordCloudI(text).generate_word_cloud(), interpolation='bilinear')
        self.view.mpl_canvas_cloud.axes.axis('off')
        self.view.mpl_canvas_cloud.setParent(self.view.frameNube)
        self.view.mpl_canvas_cloud.show()
    
    def show_hist(self):
        """Muestra el histograma.
        
        Agrega la imagen generada del histograma a su contenedor canvas
        correspondiente.
        """
        text =  " ".join(review for review in self.all_data['Texto'])
        words = WordCloudI(text, max_words=30).generate_word_cloud()
        data_list = []
        
        for key in words.words_.keys():
            data_list.append(words.words_[key])
            data_list.append(key)
            
        # self.view.mpl_canvas_hist.axes.bar(list(words.words_.keys()),words.words_.values())
        kwargs = dict(bins=30, edgecolor = 'black',  linewidth=1, color='#F2AB6D')
        self.view.mpl_canvas_hist.axes.hist(data_list, **kwargs)
        self.view.mpl_canvas_hist.axes.set_title('Frecuencia de palabras')
        self.view.mpl_canvas_hist.axes.set_ylabel('Frecuencia')
        self.view.mpl_canvas_hist.axes.set_ylabel('Palabras')
        self.view.mpl_canvas_hist.axes.tick_params(axis="x", labelrotation=90, labelsize=5)
        self.view.mpl_canvas_hist.setParent(self.view.frameHist)
        self.view.mpl_canvas_hist.show()

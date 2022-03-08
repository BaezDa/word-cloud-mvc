import os
import sys
from os.path import dirname, realpath
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from pathlib import Path
from model.neural_network import NeuralNetwork
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox
from model.word_cloud import WordCloudI

import pandas as pd
import numpy as np



scriptDir = dirname(realpath(__file__))

class MainController():
    
    def __init__(self, view, model):
        
        self.model = model
        self.view = view
        
        self.path = ""
        self.question = [0 for i in range(0, 8)]
        
        
        #Valores iniciales del modelo y spinbox        
        self.view.listView.setModel(self.model)
        # self.view.spinBox.setValue(10)

       
        #Archivo
        self.view.btnSelectFile.clicked.connect(self.select_file)
        
        #Inicio
        self.view.btnShowData.clicked.connect(self.show_data)
        self.view.btnAdd.clicked.connect(self.add)
        self.view.btnGenerate.clicked.connect(self.reduce_db)


        
        #Nube de palabras
        self.view.btnShowWordCloud.clicked.connect(self.show_cloud)
        
        
        #Histograma
        self.view.btnShowHist.clicked.connect(self.show_hist)
        
        #Red neuronal
        self.view.btnTrain_2.clicked.connect(self.train)
        
        
        self.view.btnSend_2.clicked.connect(self.send)
        self.view.checkboxActors_2.stateChanged.connect(self.onStateChange)
        self.view.checkboxCasting_2.stateChanged.connect(self.onStateChange)
        self.view.checkboxShortFilm_2.stateChanged.connect(self.onStateChange)
        self.view.checkboxCameo_2.stateChanged.connect(self.onStateChange)
        self.view.checkboxDirector_2.stateChanged.connect(self.onStateChange)
        self.view.checkboxCamera_2.stateChanged.connect(self.onStateChange)
        self.view.checkboxDubbing_2.stateChanged.connect(self.onStateChange)
        self.view.checkboxScript_2.stateChanged.connect(self.onStateChange)

    def select_file(self):
        """Selecciona el archivo CSV.
        
        Despliega una ventana donde se escoge el archivo CSV.
        
        """
        try:
            self.path = self.view.file_dialog.getOpenFileName(self.view, 'Abrir CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            self.view.lineEditPathFile.setText(self.path)
            # self.all_data = pd.read_csv(path)
        except:
            print(self.path)
            
    def save_file(self):
        """Guarda el archivo CSV.
        
        Despliega una ventana donde se escoge la ruta y el nombre
        del archivo CSV a guardar.
        
        """
        try:
            self.path = self.view.file_dialog.getSaveFileName(self.view, 'Guardar CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            print(self.path)
            return self.path
        except:
            print(self.path)

    def show_data(self):
        """Carga los datos del archivos CSV en TableWidget.
        
        Recorre el archivo CSV para asignarlos en las propiedades
        de un TableWidget.
        
        """
        self.all_data = pd.read_csv(self.path)
        
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
        text = self.view.lineEditKeyword.text()
        if text:  # No se agregan cadenas vacias.
            self.model.todos.append(text)
            self.model.layoutChanged.emit()
            self.view.lineEditKeyword.setText("")
    
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
        self.view.mpl_canvas_cloud.setParent(self.view.frameCloud)
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
            
        kwargs = dict(bins=30, edgecolor = 'black',  linewidth=0.5, color='#F2AB6D')
        self.view.mpl_canvas_hist.axes.hist(data_list, **kwargs)
        self.view.mpl_canvas_hist.axes.set_title('Frecuencia de palabras')
        self.view.mpl_canvas_hist.axes.set_ylabel('Frecuencia')
        self.view.mpl_canvas_hist.axes.set_xlabel('Palabras')
        self.view.mpl_canvas_hist.axes.tick_params(axis="x", labelrotation=90, labelsize=5, width=2, pad=-40)
        self.view.mpl_canvas_hist.setParent(self.view.frameHist)
        self.view.mpl_canvas_hist.show()
        
    def load_data(self):
        """ Carga los datos del CSV.
        
        """
        self.all_data = pd.read_csv(self.path)
        
        input_columns =  self.all_data[['Actores', 'Casting', 'Cortometraje', 'Cameo', 'Director', 'Cámara', 'Doblaje', 'Guión']]
        output_column = self.all_data[['Salida']]
        
        self.training_set_inputs = input_columns[:].values
        self.training_set_outputs = output_column.values
        
    def train(self):
        self.load_data()
        self.neural_network = NeuralNetwork()
    
        if not self.view.lineEditIterations.text():
            self.view.textBrowserInitialWeights.setText(np.array2string(self.neural_network.synaptic_weights))
            self.neural_network.train(self.training_set_inputs, self.training_set_outputs)
            self.view.textBrowserFinalWeights.setText(np.array2string(self.neural_network.synaptic_weights))
        else:
            iterations = int(self.view.lineEditIterations.text())
            self.view.textBrowserInitialWeights.setText(np.array2string(self.neural_network.synaptic_weights))
            self.neural_network.train(self.training_set_inputs, self.training_set_outputs, iterations)
            self.view.textBrowserFinalWeights.setText(np.array2string(self.neural_network.synaptic_weights))
            
        self.show_dialog()
       
    def show_dialog(self):
        dlg = QMessageBox(self.view)
        dlg.setWindowTitle("")
        dlg.setText("¡El entrenamiento ha finalizado!")
        button = dlg.exec()

        # if button == QMessageBox.Ok:
        #     print("OK!")
    
    def onStateChange(self, state):
        """ Verfica la marcación de los checkbox.
        Usa el método sender() de la vista para saber que
        checkbox ha sido marcado.
        """
        
        if state == QtCore.Qt.Checked:
            if self.view.sender() == self.view.checkboxActors_2:
                self.question[0] = 1
            elif self.view.sender() == self.view.checkboxCasting_2:
                self.question[1] = 1
            elif self.view.sender() == self.view.checkboxShortFilm_2:
                self.question[2] = 1
            elif self.view.sender() == self.view.checkboxCameo_2:
                self.question[3] = 1
            elif self.view.sender() == self.view.checkboxDirector_2:
                self.question[4] = 1
            elif self.view.sender() == self.view.checkboxCamera_2:
                self.question[5] = 1
            elif self.view.sender() == self.view.checkboxDubbing_2:
                self.question[6] = 1
            elif self.view.sender() == self.view.checkboxScript_2:
                self.question[7] = 1
        else:
            if self.view.sender() == self.view.checkboxActors_2:
                    self.question[0] = 0
            elif self.view.sender() == self.view.checkboxCasting_2:
                self.question[1] = 0
            elif self.view.sender() == self.view.checkboxShortFilm_2:
                self.question[2] = 0
            elif self.view.sender() == self.view.checkboxCameo_2:
                self.question[3] = 0
            elif self.view.sender() == self.view.checkboxDirector_2:
                self.question[4] = 0
            elif self.view.sender() == self.view.checkboxCamera_2:
                self.question[5] = 0
            elif self.view.sender() == self.view.checkboxDubbing_2:
                self.question[6] = 0
            elif self.view.sender() == self.view.checkboxScript_2:
                self.question[7] = 0
        print(self.question)
    
    def send(self):
        print (self.neural_network.think(np.array(self.question)))
        ans = np.array2string(self.neural_network.think(np.array(self.question)))
        self.view.lineEditAns.setText(ans)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 21/4/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

from sys import argv,exit
from PyQt4 import QtCore,QtGui

from platform import system
from os import getenv
from os.path import basename,dirname
from re import search
import GNSS.Teqc as teqc

class RinexViewer(QtGui.QWidget):
    '''
    classdocs
    '''
    __ftabla=None
    __btAbrir=None
    __Ficheros=[]
    __path=''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(RinexViewer, self).__init__()
        self.InitUi()
        self.setMouseTracking(True)
        
        self.connect(self.__btAbrir, QtCore.SIGNAL("clicked()"), self.AbrirRinex)
        self.connect(self.__ftabla,QtCore.SIGNAL("itemDoubleClicked (QTableWidgetItem*)"),self.AbrirGrafico)
        
        
    def InitUi(self):
        '''!
        '''
        self.setGeometry(0,0,800,600)
        grid=QtGui.QGridLayout(self)
        self.__ftabla=Tabla(0,8)
        grid.addWidget(self.__ftabla,0,0,1,0)   #Añade la tabla.
        #self.adjustSize()
        self.__btAbrir=QtGui.QPushButton('Abrir')
        self.__btAbrir.setToolTip('Pulsar para abrir Archivos')
        grid.addWidget(self.__btAbrir,1,1,1,1)
        
        #self.show()
        
        
    def AbrirRinex(self,Rutas=None):
        '''!
        '''
        if self.__path=='':
            if system()=='Linux':
                self.__path=getenv('HOME')
            elif system=='Windows':
                self.__path='C:\\'
        if Rutas==None:
            Abrir = QtGui.QFileDialog()
            Abrir.setFileMode(QtGui.QFileDialog.ExistingFiles) #Escoger multiples ficheros.
            archivos=Abrir.getOpenFileNames(self, 'Archivos Rinex ".yyd"',self.__path)
            #De vuelve los archivos con la ruta completa.
            #En el caso de que no se abra ningun archivo no se continua con la ejecución.
            if archivos == []:
                return
            self.__path=dirname(archivos[0])
        elif isinstance(Rutas,list):
            archivos=Rutas
        else:
            raise Exception('Invalido.')
        # Se añaden los ficheros a la lista.
        for i in archivos:
            if i not in self.__Ficheros:
                self.__Ficheros.append(i)
        
        cont=self.__ftabla.rowCount()
        for i in self.__Ficheros:
            #print(self.__ftabla.findItems(basename(i),QtCore.Qt.MatchExactly))
            if self.__ftabla.findItems(basename(i),QtCore.Qt.MatchExactly)==[]:
                #No existe el elemento en la tabla.
                if i.endswith("o") and search("\d\d",i.split(".")[1]):
                    cab=teqc.Teqc()
                    cabecera=cab.CabeceraRinex(i)
                    self.__ftabla.insertRow(cont)
                    self.__ftabla.setItem(cont, 0, QtGui.QTableWidgetItem(basename(i)))
                    self.__ftabla.setItem(cont, 1, QtGui.QTableWidgetItem(cabecera['NAME']))
                    self.__ftabla.setItem(cont, 2, QtGui.QTableWidgetItem(cabecera['INTERVAL']))
                    self.__ftabla.setItem(cont, 3, QtGui.QTableWidgetItem(cabecera['ANTENNA']))
                    self.__ftabla.setItem(cont, 4, QtGui.QTableWidgetItem(cabecera['DELTA N']))
                    self.__ftabla.setItem(cont, 5, QtGui.QTableWidgetItem(''))
                    self.__ftabla.setItem(cont, 6, QtGui.QTableWidgetItem(''))
                    self.__ftabla.setItem(cont, 7, QtGui.QTableWidgetItem(i))
                    
                    cont+=1
                    
            else:
                #El elemento no se vuelve a añadir ya que existe.
                continue
            
    def AbrirGrafico(self):
        '''!
        '''
        elemento=self.__ftabla.item(self.__ftabla.currentRow(),7).text()
        print(elemento)
        graf=GraficaSatelites(elemento)
        
        
        graf.show()
        graf.exec_()
                
        
    def resizeEvent(self,e):
        print(e.oldSize())
        
        
        
class GraficaSatelites(QtGui.QWidget):
    '''
    classdocs
    '''
    __scroll=None
    __graf=None
    #Satelites: GPS,GLONASS,GALILEO.
    __sats=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15",
            "16","17","18","19","20","21","22","23","24","25","26","27","28",
            "29","30","31","32","33",
              
            "R1","R2","R3","R4","R5","R6","R7","R8","R9","R10","R11","R12",
            "R13","R14","R15","R16","R17","R18","R19","R20","R21","R22","R23",
            "R24","R25",
              
            "E1","E2","E3","E4","E5","E6","E7","E8","E9","E10","E11","E12"]

    def __init__(self,ruta,parent=None):
        '''
        Constructor
        '''
        super(GraficaSatelites, self).__init__()
        self.initUi()
        
    def initUi(self):
        grid=QtGui.QGridLayout()
        scroll=QtGui.QScrollArea()
        grid.addWidget(scroll)
        self.setLayout(grid)
        #a.setLayout(grid)
        #scroll=QtGui.QScrollArea()
        scroll.setWidget(SCArea())
        #self.setLayout(grid)
        #grid.addWidget(scroll)
        
        
        #grid.addWidget(SCArea(scroll))
        #self.setCentralWidget(self.__scroll)
        #a=SCArea()
        #self.__scroll.setWidget(a)
        #grid.addWidget(self.__scroll)
        
        self.show()
        
#     def paintEvent(self,e):
#         '''!
#         '''
#         #Evento de dibujado, llamado automaticamente por el formulario.
#         #Este evento realiza todo lo que se dispone en la funcion Dibujar.
#         qp=QtGui.QPainter()
#         qp.begin(self)
#         self.Dibujar(qp)
#          
#          
#     def Dibujar(self,qp):
#         '''!
#         '''
#         for i in range(100):
#             pen=QtGui.QPen(QtGui.QColor(0, 0, 128), 4, QtCore.Qt.SolidLine)
#             qp.setPen(pen)
#             qp.drawLine(0,i*5, 100,i*5)
#             
#         qp.end()
        
        
        
class SCArea(QtGui.QWidget):
    def __init__(self,parent=None):
        '''
        Constructor
        '''
        print("hifebifbsblfbsf")
        super(SCArea, self).__init__()
        self.show()
         
         
    def paintEvent(self,e):
        '''!
        '''
        #Evento de dibujado, llamado automaticamente por el formulario.
        #Este evento realiza todo lo que se dispone en la funcion Dibujar.
        qp=QtGui.QPainter(self.viewport())
        qp.begin(self)
        QtGui.QWidget.paintEvent(self,e)
        self.Dibujar(qp)
         
         
    def Dibujar(self,qp):
        '''!
        '''
        for i in range(100):
            pen=QtGui.QPen(QtGui.QColor(0, 0, 128), 4, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(0,i*5, 100,i*5)
        qp.end()
        
        
        
class Tabla(QtGui.QTableWidget):
    '''
    classdocs
    '''
    def __init__(self,r,c):
        '''
        Constructor
        '''
        super(Tabla, self).__init__(r,c)
        self.setAcceptDrops(True)
        self.setHorizontalHeaderLabels (['NOMBRE','ESTACIÓN','ÉPOCAS','ANTENA','ALTURA ANTENA','HORA INICIO','FECHA INICIO','RUTA'])
        self.hideColumn(7)
        self.resizeColumnsToContents()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        #print(event.mimeData().urls())
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
            dlg.AbrirRinex(links)
        else:
            event.ignore()
        
        
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=RinexViewer()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()
        
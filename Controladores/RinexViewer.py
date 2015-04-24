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
from datetime import datetime

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
        self.__ftabla.resizeColumnsToContents()
            
    def AbrirGrafico(self):
        '''!
        '''
        #graf=None
        elemento=self.__ftabla.item(self.__ftabla.currentRow(),7).text()
        print(elemento)
        graf=GraficaSatelites(elemento)
        
        
        #graf.show()
        graf.exec_()
        graf=None
                
        
    def resizeEvent(self,e):
        print(e.oldSize())
        
        
        
        

        
        
        
class GraficaSatelites(QtGui.QWidget):
    '''
    classdocs
    '''
    __scroll=None
    __graf=[]
    __tini=None
    __tfin=None
    __ruta=None
    __fini=None
    __ffin=None
    __dini=None
    __dfin=None
    __dift=None
    __num_sats=None
    __tact=datetime(2000,1,1,0,0,0)
    __satelites=[]
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
        self.__ruta=ruta
        self.initUi()
        self.setMouseTracking(True)
        
        
    def initUi(self):
        '''!
        '''
        self.__graf=[]
        self.__satelites=[]
        #Posicion inicial de la ventana.
        
        #self.setGeometry(screen.width())
        #Hora interpolada.
        self.lab=QtGui.QLabel(self)
        self.lab.move(int((self.width())/2),self.height()-42)
        if self.lab.text()=="":
            self.lab.setText("00:00:00")
            
        TE=teqc.Teqc()
        sal=TE.qualityCheck(self.__ruta, borrar=True)
        sal=sal.decode().split('\n')
        #print(sal)
        #Observaciones disponibles.
        w=False
        for i in sal:
            if "Obs" in i[0:3]:
                    break
            if " SV" in i[0:3]:
                w=True
            if w:
                self.__graf.append(i)
        #Fecha de inicio y final de la observación. 
        for i in sal:
            if "Time of start of window" in i:
                self.__fini=i[26:-1]
                self.__fini=self.__fini.split(" ")
                lista = [x for x in self.__fini if x != '']
                self.__fini=[]
                self.__fini=lista
                lista=[]
##                    print(self.__fini)
            if "Time of  end  of window" in i:
                self.__ffin=i[26:-1]
                self.__ffin=self.__ffin.split(" ")
                lista = [x for x in self.__ffin if x != '']
                self.__ffin=[]
                self.__ffin=lista
                lista=[]
        #Se ordenan los satelites existentes.
        for i in sal:
            l=i[0:3]
            l=l.replace(" ", "")
            try:
                if l in self.__sats:
                    if len(set(i[4:76])) > 1:
                        self.__satelites.append(i)
                    elif len(set(i[4:76]))==1 and list(set(i[4:76]))[0]!=" ":
                        self.__satelites.append(i)
            except:
                continue
        self.__satelites.sort()
        
        self.__num_sats=len(self.__satelites)
        self.__tini=self.__fini[-1].split(":")
        self.__tfin=self.__ffin[-1].split(":")

        self.__dini=datetime(2000,1,1,int(self.__tini[0]),int(self.__tini[1]),int(float(self.__tini[2])))
        self.__dfin=datetime(2000,1,1,int(self.__tfin[0]),int(self.__tfin[1]),int(float(self.__tfin[2])))

        self.__dift=self.__dfin-self.__dini
            
        self.show()
        
    def mouseMoveEvent(self, event):
        '''
        Evento automático, que se ejecuta de forma automatica.
        En este caso lo que se realiza es un interpolacion de la posicion del
        ratón el área gráfica, con las horas mínima y máxima de el fichero.
        '''
        if event.pos().x()>=50 and event.pos().x()<=self.width() and event.pos().y()<self.height()-50:
            ancho=self.width()-51
            self.__tact=self.__dini+((event.pos().x()-50)/ancho)*self.__dift
            self.lab.setText(str(self.__tact.time())[0:8])
        
    def paintEvent(self,e):
        '''
        Evento de dibujado, llamado automaticamente por el formulario.
        Este evento realiza todo lo que se dispone en la funcion Dibujar.
        '''
        qp=QtGui.QPainter()
        qp.begin(self)
        self.Dibujar(qp)
        
        
    def Dibujar(self,qp):
        '''!
        '''
        #Tamaño de la fuente.
        #Debera ser variable en fución del número de satélites.
        tf=7
        #Margenes.
        qp.setBrush(QtGui.QColor(75, 75, 75))
        rect =QtCore.QRect(50,0,self.width(),self.height()-50)
        qp.drawRect(rect)
        
        anchosat=(self.height()-50)/self.__num_sats
        print(anchosat)
        #Dibujar la rejilla.
        pen = QtGui.QPen(QtCore.Qt.black, 1)
        qp.setPen(pen)
        qp.drawLine(50,0,50,self.height())
        for i in range(self.__num_sats):
            i+=1
            qp.drawLine(0, i*anchosat, self.width(), i*anchosat)
        #Dibujar los nombres de los satélites.
        Fuente=QtGui.QFont("Arial",tf)
        qp.setFont(Fuente)
        val=(anchosat/2)+0.5*tf
        for i in self.__satelites:
            qp.drawText(20,val,i[0:3]) 
            val+=anchosat
        val=None
        
        gl=1 #Grosor de la linea.
        if anchosat<=10:
            gl=1
            val=(anchosat/2)
        else:
            gl=3
            val=(anchosat/2)-1.5*gl
        
        for i in self.__satelites:
            elem=i[4:76]
            escal=(self.width()-50)/72
##            print(elem)
            k=51
            t=0
            #Se dibuja la linea con la observación al satelite.
            for j in elem:
                t=k+escal
                #Modo agrupado para pintar las lineas del satelite de un mismo color.
                if "N" in j or "_" in j or " " in j or "-" in j or "I" in j or "M" in j or "c" in j:
                    qp.setPen(QtGui.QColor(0, 0, 0,0))
                    qp.drawLine(k, 5+val, t,5+val)
                    
                if "1" in j or "C" in j or "o" in j or "L" in j or "m" in j or "+" in j or "a" in j or "^" in j or "," in j or "?" in j or "~" in j or "N" in j:
                    pen=QtGui.QPen(QtGui.QColor(0, 0, 128), gl, QtCore.Qt.SolidLine)
                    qp.setPen(pen)
                    qp.drawLine(k, 5+val, t,5+val)
                    
                k+=escal
            val+=anchosat
            
        pen = QtGui.QPen(QtCore.Qt.black, 1)
        qp.setPen(pen)
        #Se resalta el color de la hora inicial y final
        Fuente=QtGui.QFont("Arial",9)
        Fuente.setBold(True)
        Fuente.setUnderline(False)
        pen=QtGui.QPen(QtGui.QColor(0, 0, 0), 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(Fuente)     
        #Hora inicial.
        qp.drawText(55,(self.height()-50)+9+2,str(self.__tini[0])+":"+str(self.__tini[1])+":"+str(self.__tini[2].split(".")[0]))
        qp.drawText(55,(self.height()-50)+25,str(self.__fini[2])+" "+str(self.__fini[1])+" "+str(self.__fini[0]))
        #Hora final.
        qp.drawText(self.width()-50,(self.height()-50)+9+2,str(self.__tfin[0])+":"+str(self.__tfin[1])+":"+str(self.__tfin[2].split(".")[0]))
        qp.drawText(self.width()-71,(self.height()-50)+25,str(self.__ffin[2])+" "+str(self.__ffin[1])+" "+str(self.__ffin[0]))
        #Hora interpolada.
        Fuente=QtGui.QFont("Arial",10)
        Fuente.setBold(True)
        Fuente.setUnderline(False)
        pen=QtGui.QPen(QtGui.QColor(0, 0, 128), 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(Fuente)
        self.lab.move(int((self.width()-50)/2),(self.height()-50)+9+2)
        
        qp.end()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#     def initUi(self):
#         grid=QtGui.QGridLayout()
#         scroll=QtGui.QScrollArea()
#         grid.addWidget(scroll)
#         self.setLayout(grid)
        #a.setLayout(grid)
        #scroll=QtGui.QScrollArea()
#         scroll.setWidget(SCArea())
        #self.setLayout(grid)
        #grid.addWidget(scroll)
        
        
        #grid.addWidget(SCArea(scroll))
        #self.setCentralWidget(self.__scroll)
        #a=SCArea()
        #self.__scroll.setWidget(a)
        #grid.addWidget(self.__scroll)
        
#         self.show()
        
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
        
        
        
# class SCArea(QtGui.QWidget):
#     def __init__(self,parent=None):
#         '''
#         Constructor
#         '''
#         print("hifebifbsblfbsf")
#         super(SCArea, self).__init__()
#         self.show()
#          
#          
#     def paintEvent(self,e):
#         '''!
#         '''
        #Evento de dibujado, llamado automaticamente por el formulario.
        #Este evento realiza todo lo que se dispone en la funcion Dibujar.
#         qp=QtGui.QPainter(self.viewport())
#         qp.begin(self)
#         QtGui.QWidget.paintEvent(self,e)
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
#         qp.end()
        
        
        
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
        self.setToolTip('Abra o arrastre archivos Rinex Standard.')
        
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
            self.resizeColumnsToContents()
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
        
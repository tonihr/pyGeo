#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 17/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from os import sep,pardir,getcwd
from os.path import normpath
import Geometrias.PuntoUTM
import Proyecciones.UTM2Geo
import Geodesia.EGM.CalcularOndulacionTxt

class UTM2Geo(QtGui.QWidget):
    '''
    classdocs
    '''
    __rutaroot=None
    __msgBoxErr=None
    __pLat=None
    __pLon=None
    __pw=None
    __pN=None


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(UTM2Geo, self).__init__()
        #Se carga el formulario para el controlador.
        self.__rutaroot=normpath(getcwd() + sep + pardir)
        uic.loadUi(self.__rutaroot+'/Formularios/UTM2Geo.ui', self)
        self.__msgBoxErr=QtGui.QMessageBox()
        self.__msgBoxErr.setWindowTitle("ERROR")  
        self.__CargarElipsoides()
        self.__tabChanged()
        self.__setPrecision()
        self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.Calcular)
        self.connect(self.pushButton_4, QtCore.SIGNAL("clicked()"), self.launch)
        self.connect(self.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.__tabChanged)
        self.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.AbrirFicheroUTM)
        self.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), self.AbrirFicheroGeo)
        self.connect(self.spinBox_2, QtCore.SIGNAL("valueChanged (int)"), self.__setPrecision)
        self.connect(self.spinBox_3, QtCore.SIGNAL("valueChanged (int)"), self.__setPrecision)
        self.connect(self.spinBox_4, QtCore.SIGNAL("valueChanged (int)"), self.__setPrecision)
        self.connect(self.spinBox_5, QtCore.SIGNAL("valueChanged (int)"), self.__setPrecision)
        
        
        
    def __CargarElipsoides(self):
        '''!
        '''
        import BasesDeDatos.SQLite.SQLiteManager
        try:
            db=BasesDeDatos.SQLite.SQLiteManager.SQLiteManager(self.__rutaroot+'/Geodesia/Elipsoides/Elipsoides.db')
            Nombres=db.ObtenerColumna('Elipsoides','Nombre')
            Nombres=[i[0] for i in Nombres]
            Nombres.sort()
            self.comboBox.addItems(Nombres)
            self.comboBox.setCurrentIndex(28)
            self.comboBox_2.addItems(Nombres)
            self.comboBox_2.setCurrentIndex(28)
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        
        
    def Calcular(self):
        '''!
        '''
        putm=None
        if self.lineEdit.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para la X UTM.")
            self.__msgBoxErr.exec_()
            return
        if self.lineEdit_2.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para la Y UTM.")
            self.__msgBoxErr.exec_()
            return
        try:
            putm=Geometrias.PuntoUTM.PuntoUTM(self.lineEdit.text(),self.lineEdit_2.text(),huso=self.spinBox.value())
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        Sal=None
        try:
            Sal=Proyecciones.UTM2Geo.UTM2Geo(putm, self.comboBox.currentText())
            self.lineEdit_3.setText(str(round(Sal.getLatitud(),self.__pLat)))
            self.lineEdit_4.setText(str(round(Sal.getLongitud(),self.__pLon)))
            self.lineEdit_5.setText(str(round(putm.getConvergenciaMeridianos(),self.__pw)))
            self.lineEdit_6.setText(str(putm.getEscalaLocalPunto()))
            try:
                self.lineEdit_7.setText(str(round(Geodesia.EGM.CalcularOndulacionTxt.CalcularOndulacion(Sal),self.__pN)))
            except:
                self.lineEdit_7.setText("")

        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        
    def AbrirFicheroUTM(self):
        '''!
        '''
        ruta = QtGui.QFileDialog.getOpenFileName(self, 'Abrir Archivo', '.')
        self.lineEdit_9.setText(ruta)
        
    def AbrirFicheroGeo(self):
        '''!
        '''
        ruta = QtGui.QFileDialog.getSaveFileName(self, 'Guadar Archivo', '.')
        self.lineEdit_10.setText(ruta)
        
    def launch(self):
        '''!
        '''
        QtCore.QThread(self.CalcularArchivo()).exec_()
        
        
    def CalcularArchivo(self):
        '''!
        '''
        pd=QtGui.QProgressDialog()
        
        if self.lineEdit_9.text()=="":
            self.__msgBoxErr.setText("Debe introducir un fichero de coordenadas UTM.")
            self.__msgBoxErr.exec_()
            return
        if self.lineEdit_10.text()=="":
            self.__msgBoxErr.setText("Debe introducir un fichero de salida para las coordenadas Geodesicas")
            self.__msgBoxErr.exec_()
            return
        #Formato del fichero de coordenadas Geodesicas.
        #ID,X,Y,posY,Huso,helip(opcional)
        pd.show()
        pd.setLabelText("Tarea 1..2 Procesando el fichero.")
        
        try:
            QtGui.QApplication.processEvents()
            sal=Proyecciones.UTM2Geo.UTM2GeoFromFile(self.lineEdit_9.text(), self.comboBox_2.currentText())
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        pg=QtGui.QProgressBar(pd)
        pd.setBar(pg)
        pg.setMinimum(0)
        pg.setMaximum(len(sal))
        
        g=open(self.lineEdit_10.text(),'w')
        pd.setLabelText("Tarea 2..2 Escribiendo nuevo fichero.")
        cont=0
        pg.show()
        for i in sal:
            QtGui.QApplication.processEvents()
            line=""
            line+=i[0]+","
            line+=str(round(i[2].getLatitud(),self.__pLat))+","
            line+=str(round(i[2].getLongitud(),self.__pLon))+","
            h=i[2].getAlturaElipsoidal()
            if h==None:
                line+","
            else:
                line+=str(h)+","
            line+=str(i[1].getHuso())+","
            line+=str(round(i[1].getConvergenciaMeridianos(),self.__pw))+","
            line+=str(round(i[1].getEscalaLocalPunto(),self.__pw))+","
            line+=str(i[1].getZonaUTM())+"\n"
            g.write(line)
            pg.setValue(cont)
            cont+=1
        g.close()
        pg.hide()
        
    def __setPrecision(self):
        '''!
        '''
        self.__pLat=self.spinBox_2.value()
        self.__pLon=self.spinBox_3.value()
        self.__pw=self.spinBox_4.value()
        self.__pN=self.spinBox_5.value()
        
        
    def __tabChanged(self):
        '''!
        '''
        if self.tabWidget.currentIndex()==0:
            self.setFixedSize ( 319, 490)
        elif self.tabWidget.currentIndex()==1:
            self.setFixedSize ( 562, 272)
            pass
        elif self.tabWidget.currentIndex()==2:
            self.setFixedSize ( 354, 202)
            pass
        
        
        
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(sys.argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=UTM2Geo()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    sys.exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()
        
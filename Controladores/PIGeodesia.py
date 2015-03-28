#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 9/3/2015

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
import Geodesia.PIGeodesia as pig
import Geometrias.PuntoGeodesico as pgeo
import Geometrias.Angulo as ang
import Geodesia.RadiosDeCurvatura as rcurv


class PIGeodesia(QtGui.QWidget):
    '''!
    classdocs
    '''


    def __init__(self, parent=None):
        '''!
        Constructor
        '''
        super(PIGeodesia, self).__init__()
        #Se carga el formulario para el controlador.
        self.__rutaroot=normpath(getcwd() + sep + pardir)
        uic.loadUi(self.__rutaroot+'/Formularios/PIGeodesia.ui', self)
        self.__msgBoxErr=QtGui.QMessageBox()
        self.__msgBoxErr.setWindowTitle("ERROR")
        self.setFixedSize(270,354)
        self.__CargarElipsoides()
        self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.Calcular)
        
        
        
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
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        
        
    def Calcular(self):
        '''!
        '''
        if self.lineEdit.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para la latitud origen.")
            self.__msgBoxErr.exec_()
            return
        if self.lineEdit_2.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para la la longitud origen.")
            self.__msgBoxErr.exec_()
            return
        if self.lineEdit_3.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para la latitud destino.")
            self.__msgBoxErr.exec_()
            return
        if self.lineEdit_4.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para la la longitud destino.")
            self.__msgBoxErr.exec_()
            return
        
        try:
            sal=pig.PIGeodesia(pgeo.PuntoGeodesico(self.lineEdit.text(),self.lineEdit_2.text()),pgeo.PuntoGeodesico(self.lineEdit_3.text(),self.lineEdit_4.text()))   
            az,d=sal.CalcularBessel(self.comboBox.currentText())
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            
        a1=ang.Angulo(az,girar=True)
        a1.Convertir('pseudosexagesimal')
        self.lineEdit_6.setText(str(a1.getAngulo()))
        Radio=rcurv.RadiosDeCurvatura(self.comboBox.currentText())
        nhu1=Radio.getRadioPrimerVertical(float(self.lineEdit.text()))
        ro1=Radio.getRadioElipseMeridiana(float(self.lineEdit.text()))
        nhu2=Radio.getRadioPrimerVertical(float(self.lineEdit_3.text()))
        ro2=Radio.getRadioElipseMeridiana(float(self.lineEdit_3.text()))
        from math import sqrt
        Rm=(1/2)*((sqrt(nhu1*ro1))+(sqrt(nhu2*ro2)))
        self.lineEdit_5.setText(str(d*Rm))
        
        
        
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(sys.argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=PIGeodesia()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    sys.exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()
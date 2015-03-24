#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 6/3/2015

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
import Geodesia.PDGeodesia as pdg
import Geometrias.PuntoGeodesico as pgeo
import Geometrias.Angulo as ang

class PDGeodesia(QtGui.QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(PDGeodesia, self).__init__()
        #Se carga el formulario para el controlador.
        self.__rutaroot=normpath(getcwd() + sep + pardir)
        uic.loadUi(self.__rutaroot+'/Formularios/PDGeodesia.ui', self)
        self.__msgBoxErr=QtGui.QMessageBox()
        self.__msgBoxErr.setWindowTitle("ERROR")
        self.setFixedSize(274,422)
        self.__CargarElipsoides()
        self.__CheckBox()
        self.connect(self.checkBox, QtCore.SIGNAL("stateChanged (int)"), self.__CheckBox)
        self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.Calcular)
        
        
    def __CargarElipsoides(self):
        '''!
        '''
        import BasesDeDatos.SQLite.SQLiteManager
        try:
            db=BasesDeDatos.SQLite.SQLiteManager.SQLiteManager(self.__rutaroot+'/Geodesia/Elipsoides/Elipsoides.db')
            Nombres=db.ObtenerColumna('Nombre', 'Elipsoides')
            Nombres=[i[0] for i in Nombres]
            Nombres.sort()
            self.comboBox.addItems(Nombres)
            self.comboBox.setCurrentIndex(28)
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        
    def __CheckBox(self):
        '''!
        '''
        if self.checkBox.checkState()==2:
            self.lineEdit_7.setEnabled(True)
        elif self.checkBox.checkState()==0:
            self.lineEdit_7.setEnabled(False)
            
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
            self.__msgBoxErr.setText("Debe introducir un valor para la distancia de calculo.")
            self.__msgBoxErr.exec_()
            return
        if self.lineEdit_4.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para el azimut.")
            self.__msgBoxErr.exec_()
            return
        
        pasos=None
        if self.checkBox.checkState()==2:
            try:
                int(self.lineEdit_7.text())
            except:
                self.__msgBoxErr.setText("El número de pasos debe ser un valor entero.")
                self.__msgBoxErr.exec_()
                return
            finally:
                pasos=int(self.lineEdit_7.text())
        try:   
            sal=pdg.PDGeodesia(pgeo.PuntoGeodesico(self.lineEdit.text(),self.lineEdit_2.text()),self.lineEdit_3.text(),self.lineEdit_4.text())
            lat,lon,az=sal.Rk4o(self.comboBox.currentText(), pasos)
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            
        #ang.Angulo(lat).Convertir('pseudosexagesimal').getAngulo()
        a1=ang.Angulo(lat,girar=True)
        a1.Convertir('pseudosexagesimal')
        self.lineEdit_6.setText(str(a1.getAngulo()))
        a1=ang.Angulo(lon,girar=True)
        a1.Convertir('pseudosexagesimal')
        self.lineEdit_5.setText(str(a1.getAngulo()))
        a1=ang.Angulo(az,girar=True)
        a1.Convertir('pseudosexagesimal')
        self.lineEdit_8.setText(str(a1.getAngulo()))
            
        
            
        
        
        
        
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(sys.argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=PDGeodesia()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    sys.exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()
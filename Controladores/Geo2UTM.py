#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 10/2/2015

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
import Geometrias.PuntoGeodesico
import Proyecciones.Geo2UTM
import Geodesia.EGM.CalcularOndulacion


class Geo2UTM(QtGui.QWidget):
    '''!
    classdocs
    '''
    __rutaroot=None
    __msgBoxErr=None
    #Precisiones.
    __px=None
    __py=None
    __pw=None
    __pkp=None
    __pN=None


    def __init__(self, parent=None):
        '''!
        Constructor
        '''
        super(Geo2UTM, self).__init__()
        #Se carga el formulario para el controlador.
        self.__rutaroot=normpath(getcwd() + sep + pardir)
        uic.loadUi(self.__rutaroot+'/Formularios/Geo2UTM.ui', self)
        self.__msgBoxErr=QtGui.QMessageBox()
        self.__msgBoxErr.setWindowTitle("ERROR")  
        self.__CargarElipsoides()
        self.__tabChanged()
        self.__setPrecision()
        self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.Calcular)
        self.connect(self.pushButton_4, QtCore.SIGNAL("clicked()"), self.launch)
        self.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.AbrirFicheroGeo)
        self.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), self.AbrirFicheroUTM)
        self.connect(self.checkBox, QtCore.SIGNAL("stateChanged (int)"), self.__ForzarHuso)
        self.connect(self.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.__tabChanged)
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
            Nombres=db.ObtenerColumna( 'Elipsoides','Nombre')
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
        
    def __ForzarHuso(self):
        '''!
        '''
        if self.checkBox.isChecked():
            self.spinBox.setEnabled(True)
        else:
            self.spinBox.setEnabled(False)
            
    def launch(self):
        '''!
        '''
        QtCore.QThread(self.CalcularArchivo()).exec_()
#         p = Process(target=self.CalcularArchivo)
#         p.start()
#         p.join()
        
        
    def Calcular(self):
        '''!
        '''
        if self.lineEdit.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para la Latitud.")
            self.__msgBoxErr.exec_()
            return
        if self.lineEdit_2.text()=="":
            self.__msgBoxErr.setText("Debe introducir un valor para la Longitud.")
            self.__msgBoxErr.exec_()
            return
        try:
            pgeo=Geometrias.PuntoGeodesico.PuntoGeodesico(self.lineEdit.text(),self.lineEdit_2.text())
            if self.lineEdit_3.text()!="":
                pgeo.setAlturaElipsoidal(self.lineEdit_3.text())
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        
        Sal=None
        try:
            if self.spinBox.isEnabled():
                Huso=self.spinBox.value()
            else:
                Huso=None
            Sal=Proyecciones.Geo2UTM.Geo2UTM(pgeo, self.comboBox.currentText(), Huso)
            self.lineEdit_4.setText(str(round(Sal.getX(),self.__px)))
            self.lineEdit_5.setText(str(round(Sal.getY(),self.__py)))
            self.lineEdit_6.setText(str(Sal.getHuso()))
            self.lineEdit_12.setText(str(Sal.getZonaUTM()))
            self.lineEdit_7.setText(str(round(Sal.getConvergenciaMeridianos(),self.__pw)))
            self.lineEdit_8.setText(str(round(Sal.getEscalaLocalPunto(),self.__pkp)))
            try:
                self.lineEdit_9.setText(str(round(Geodesia.EGM.CalcularOndulacion.CalcularOndulacion(pgeo),self.__pN)))
            except Exception as e:
                print(e)
                self.lineEdit_9.setText("")
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        
    def AbrirFicheroGeo(self):
        '''!
        '''
        ruta = QtGui.QFileDialog.getOpenFileName(self, 'Abrir Archivo', '.')
        self.lineEdit_10.setText(ruta)
        
    def AbrirFicheroUTM(self):
        '''!
        '''
        ruta = QtGui.QFileDialog.getSaveFileName(self, 'Guadar Archivo', '.')
        self.lineEdit_11.setText(ruta)
        
        
    def CalcularArchivo(self):
        '''!
        '''
        pd=QtGui.QProgressDialog()
        #QtGui.QApplication.processEvents()
        if self.lineEdit_10.text()=="":
            self.__msgBoxErr.setText("Debe introducir un fichero de coordenadas geodesicas.")
            self.__msgBoxErr.exec_()
            return
        if self.lineEdit_11.text()=="":
            self.__msgBoxErr.setText("Debe introducir un fichero de salida para las coordenadas UTM..")
            self.__msgBoxErr.exec_()
            return
        
        #Formato del fichero de coordenadas Geodesicas.
        #ID,Latitud,Longitud,helip(opcional),ForzarHuso(opcional)
        pd.show()
        pd.setLabelText("Tarea 1..2 Procesando el fichero.")
        
        try:
            QtGui.QApplication.processEvents()
            sal=Proyecciones.Geo2UTM.Geo2UTMFromFile(self.lineEdit_10.text(), self.comboBox_2.currentText())
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        pg=QtGui.QProgressBar(pd)
        pd.setBar(pg)
        pg.setMinimum(0)
        pg.setMaximum(len(sal))
        cont=0
        #X,Y,Hemis,Huso,Convm,kp,N,zona
        pd.setLabelText("Tarea 2..2 Escribiendo nuevo fichero.")
        
        with open(self.lineEdit_11.text(),'w') as f:
            pg.show()
            for i in sal:
                QtGui.QApplication.processEvents()
                line=""
                line+=i[0]+","
                line+=str(round(i[2].getX(),self.__px))+","
                line+=str(round(i[2].getY(),self.__py))+","
                line+=str(i[2].getHemisferioY())+","
                line+=str(i[2].getHuso())+","
                line+=str(round(i[2].getConvergenciaMeridianos(),self.__pw))+","
                line+=str(round(i[2].getEscalaLocalPunto(),self.__pkp))+","
                try:
                    line+=str(round(Geodesia.EGM.CalcularOndulacion.CalcularOndulacion(i[1]),self.__pN))+","
                except:
                    line+=","
                line+=str(i[2].getZonaUTM())+"\n"
                f.write(line)
                pg.setValue(cont)
                cont+=1
            f.close()
            pg.hide()
            
    def __setPrecision(self):
        '''!
        '''
        self.__px=self.spinBox_2.value()
        self.__py=self.spinBox_3.value()
        self.__pw=self.spinBox_4.value()
        self.__pkp=self.spinBox_5.value()
        self.__pN=self.spinBox_6.value()
                
            
        
    def __tabChanged(self):
        '''!
        '''
        if self.tabWidget.currentIndex()==0:
            self.setFixedSize ( 334, 571)
        elif self.tabWidget.currentIndex()==1:
            self.setFixedSize ( 562, 272)
            pass
        elif self.tabWidget.currentIndex()==2:
            self.setFixedSize ( 344, 242)
            pass
        
            
        
        
        
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(sys.argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=Geo2UTM()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    sys.exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()

#     with Geo2UTM() as dlg:
#         if dlg:
#             dlg.show()
#             sys.exit(app.exec_())
#             app.close()
    
    
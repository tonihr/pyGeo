'''
Created on 18/2/2015

@author: toni
'''
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from os import sep,pardir,getcwd
from os.path import normpath
import Geometrias.Angulo as ang

class CalcAng(QtGui.QWidget):
    '''
    classdocs
    '''
    __rutaroot=None
    __msgBoxErr=None
    __tipos=ang.Angulo().getFormatosDisponibles()


    def __init__(self, parent=None):
        '''!
        Constructor
        '''
        super(CalcAng, self).__init__()
        #Se carga el formulario para el controlador.
        self.__rutaroot=normpath(getcwd() + sep + pardir)
        uic.loadUi(self.__rutaroot+'/Formularios/AngularCalc.ui', self)
        self.__msgBoxErr=QtGui.QMessageBox()
        self.__tabChanged()
        self.__RellenarCombos()
        self.connect(self.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.__tabChanged)
        self.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.__RellenarCombos)
        self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.Convertir)
        self.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.AbrirFicheroAngulos)
        self.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), self.AbrirFicheroResultados)
                
        
    def __RellenarCombos(self):
        '''!
        '''
        for i in self.__tipos:
            if not i in [self.comboBox.itemText(i) for i in range(self.comboBox.count())]:
                self.comboBox.addItem(i)
            if not i in [self.comboBox_2.itemText(i) for i in range(self.comboBox_2.count())]:
                self.comboBox_2.addItem(i)
        txt1=self.comboBox.currentText()
        i2=self.comboBox_2.findText(txt1)
        self.comboBox_2.removeItem(i2)
        
    def Convertir(self):
        '''
        '''
        try:
            c1=self.comboBox.currentText()
            a1=self.lineEdit.text()
            if c1!='sexagesimal' and "º" in a1:
                self.__msgBoxErr.setText("El valor del ángulo introducido sólo es admito para la conversión sexagesimal.")
                self.__msgBoxErr.exec_()
                return
            c2=self.comboBox_2.currentText()
            if c1=='sexagesimal':
                g=a1[0:2]
                m=a1[3:5]
                s=a1[6:]
                #print(g,m,s)
                ang1=ang.Angulo(g,m,s)
                ang1.Convertir(c2)
                self.lineEdit_2.setText(str(ang1.getAngulo()))
                
            else:
                ang1=ang.Angulo(a1,formato=c1)
                ang1.Convertir(c2)
                if c2=='sexagesimal':
                    g=str(int(ang1.getAngulo()[0]))
                    m=str(int(ang1.getAngulo()[1]))
                    s=str(ang1.getAngulo()[2])
                    self.lineEdit_2.setText(g+"º"+m+"'"+s)
                else:
                    self.lineEdit_2.setText(str(ang1.getAngulo()))
                pass
            
        except Exception as e:
            self.__msgBoxErr.setText(e.__str__())
            self.__msgBoxErr.exec_()
            return
        
    def AbrirFicheroAngulos(self):
        '''!
        '''
        ruta = QtGui.QFileDialog.getOpenFileName(self, 'Abrir Archivo', '.')
        self.lineEdit_3.setText(ruta)
        
    def AbrirFicheroResultados(self):
        '''!
        '''
        ruta = QtGui.QFileDialog.getSaveFileName(self, 'Guadar Archivo', '.')
        self.lineEdit_4.setText(ruta)
        
    def ConvertirFichero(self):
        '''!
        '''
        with open(self.lineEdit_3.text(),'r') as f:
            for i in f:
                QtGui.QApplication.processEvents()
                lin=i.split(",")
                if len(lin)==2:
                    #Radian a ...
                    ang1=ang.Angulo(lin[0])
                    ang1.Convertir(lin[1])
                    continue
                if len(lin)==3:
                    # De f1 a f2
                    ang1=ang.Angulo(lin[0],formato=lin[1])
                    ang1.Convertir(lin[2])
                    continue
                if len(lin)==4:
                    #Sexagesimal a...
                    ang1=ang.Angulo(lin[0],lin[1],lin[2])
                    ang1.Convertir(lin[3])
                    continue
                if len(lin)==5:
                    #Sexagesimal a ...
                    ang1=ang.Angulo(lin[0],lin[1],lin[2])
                    if lin[3]!='sexagesimal':
                        self.__msgBoxErr.setText("El único formato admisible de cambio es sexagesimal.")
                        self.__msgBoxErr.exec_()
                        return
                    else:
                        ang1.Convertir(lin[4])
            f.close()     
                    
        
    def __tabChanged(self):
        '''!
        '''
        if self.tabWidget.currentIndex()==0:
            self.setFixedSize ( 502, 132)
        elif self.tabWidget.currentIndex()==1:
            self.setFixedSize ( 502, 400)
            pass
        elif self.tabWidget.currentIndex()==2:
            self.setFixedSize ( 360, 120)
            pass
        
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(sys.argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=CalcAng()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    sys.exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()
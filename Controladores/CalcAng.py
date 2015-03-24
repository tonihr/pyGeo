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
import Geometrias.Angulo

class CalcAng(QtGui.QWidget):
    '''
    classdocs
    '''
    __rutaroot=None
    __msgBoxErr=None
    __tipos=Geometrias.Angulo.Angulo().getFormatosDisponibles()


    def __init__(self, parent=None):
        '''!
        Constructor
        '''
        super(CalcAng, self).__init__()
        #Se carga el formulario para el controlador.
        self.__rutaroot=normpath(getcwd() + sep + pardir)
        uic.loadUi(self.__rutaroot+'/Formularios/AngularCalc.ui', self)
        self.__msgBoxErr=QtGui.QMessageBox()
        self.__RellenarCombos()
        self.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.__RellenarCombos)
        
        
        
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
        
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(sys.argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=CalcAng()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    sys.exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()
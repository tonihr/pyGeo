#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 7/5/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from sys import argv,exit
from PyQt4 import QtCore,QtGui,uic
from os import sep,pardir,getcwd
from os.path import normpath

class RinexManagment(QtGui.QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(RinexManagment, self).__init__()
        #Se carga el formulario para el controlador.
        self.__rutaroot=normpath(getcwd() + sep + pardir)
        uic.loadUi(self.__rutaroot+'/Formularios/RinexManagment.ui', self)
        
        self.listWidget=Lista()
        self.gridLayout_2.addWidget(self.listWidget,0,0)
        self.setMouseTracking(True)
    
    
    
class Lista(QtGui.QListWidget):
    '''
    classdocs
    '''
    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(Lista, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setToolTip('Abra o arrastre archivos Rinex Standard.')
        print('iniciado')
        
    def dragEnterEvent(self, event):
        print('Sa cogio')
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        print('Sa movio')
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
            self.addItems(links)
        else:
            event.ignore()
            
            
            
            
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=RinexManagment()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()
        
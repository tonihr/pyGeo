#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 30/4/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from PyQt4 import QtCore,QtGui,QtOpenGL
from sys import argv,exit

class Viewer3D(QtOpenGL.QGLWidget):
    '''!
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(Viewer3D, self).__init__()
        self.setMouseTracking(True)
        
    def initializeGL(self):
        '''!
        '''
        print('inicia')
        
    def paintGL(self):
        '''!
        '''
        self.qglClearColor(QtGui.QColor(255,0,0))
        
        
        
if __name__ == "__main__":
    #arranque del programa.
    app = QtGui.QApplication(argv)#requerido en todas las aplicaciones con cuadros de diálogo.

    dlg=Viewer3D()#creo un objeto de nuestro controlador del cuadro.
    dlg.show()
##    dlg.exec_()
  
    exit(app.exec_())#Requerido. Al cerrar el cuadro termina la aplicación
    app.close()
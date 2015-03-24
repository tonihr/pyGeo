#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 10/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Intersecciones.Interseccion2D as i2d
import Geometrias.Linea2D as l2d
import Geometrias.Punto2D as pt2

class MultipleInterseccion2D(object):
    '''
    classdocs
    '''
    __lins=None


    def __init__(self, Lineas):
        '''
        Constructor de la clase MultipleInterseccion2D.
        '''
        self.setLines(Lineas)
        
    def setLines(self,Lineas):
        '''!
        '''
        if not isinstance(Lineas, list):
            raise Exception("Se esperaba una lista como argumento de entrada.")
        
        for indi,i in enumerate(Lineas):
            if not isinstance(i, l2d.Linea2D):
                raise Exception("El elemento: "+str(indi)+" introducido no es un objeto de la clase Linea2D.")
        self.__lins=Lineas 
        
            
    def Intersectar(self):
        '''!
        '''
        sal=[]
        for indi1,i in enumerate(self.__lins):
            for indi2,j in enumerate(self.__lins):
                if indi1==indi2 or indi1>indi2:
                    continue
                else:
                    inter=i2d.Interseccion2D(i,j)
                    sal.append([indi1,indi2,inter.Intersectar(tipo='virtual')])
        return sal
        
        
def main():

    Lineas=[l2d.Linea2D(pt2.Punto2D(0.0,0.0),pt2.Punto2D(10,10)),
            l2d.Linea2D(pt2.Punto2D(0.0,10),pt2.Punto2D(0.0,-5.0)),
            l2d.Linea2D(pt2.Punto2D(0.0,0.0),pt2.Punto2D(10.0,0.0)),
            l2d.Linea2D(pt2.Punto2D(20,50),pt2.Punto2D(40,30)),
            l2d.Linea2D(pt2.Punto2D(-10,-10),pt2.Punto2D(-10,10)),
            l2d.Linea2D(pt2.Punto2D(-10,10),pt2.Punto2D(10,10))]
    
    mi2d=MultipleInterseccion2D(Lineas)
    sal=mi2d.Intersectar()
    for i in sal:
        if i[2]==None:
            print(i[0],i[1],'No intersectan')
        else:
            print(i[0],i[1],i[2].getX(),i[2].getY())


    #a1=0
    #a2=N
    #b1=0
    #b2=-10
    
if __name__=="__main__":
    main()
            
        
        
        
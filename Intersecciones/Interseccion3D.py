#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 30/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

import Geometrias.Linea3D as l3d
import Geometrias.Punto3D as pt3
from numpy import matrix,array
from numpy.linalg import det,lstsq

class Interseccion3D(object):
    '''
    classdocs
    '''
    __l1=None
    __l2=None


    def __init__(self, Linea3D1,Linea3D2):
        '''
        Constructor
        '''
        self.__checkFirstLine(Linea3D1)
        self.setFirstLine(Linea3D1)
        self.__checkSecondLine(Linea3D2)
        self.setSecondLine(Linea3D2)
        
        
    def __checkFirstLine(self,Linea3D1):
        '''!
        @brief: Método que comprueba la primera línea introducida.
        @param Linea3D1 Linea3D: Objeto de la clase Linea3D.
        '''
        
        if not isinstance(Linea3D1, l3d.Linea3D):
            raise Exception("Se esperaba un objeto de la clase Linea3D como primer valor de entrada.")
        
    def __checkSecondLine(self,Linea3D2):
        '''!
        @brief: Método que comprueba la primera línea introducida.
        @param Linea2D1 Linea2D: Objeto de la clase Linea3D.
        '''
        
        if not isinstance(Linea3D2, l3d.Linea3D):
            raise Exception("Se esperaba un objeto de la clase Linea3D como segundo valor de entrada.")
        
    def setFirstLine(self,Linea3D1):
        '''!
        @brief: Método para introducir la primera línea de cálculo.
        @param Linea3D1 Linea3D: Objeto de la clase Linea2D.
        '''
        self.__l1=Linea3D1
        
    def setSecondLine(self,Linea3D2):
        '''!
        @brief: Método para introducir la primera línea de cálculo.
        @param Linea3D1 Linea3D: Objeto de la clase Linea3D.
        '''
        self.__l2=Linea3D2
        
    def __checkTipo(self,tipo):
        '''
        @brief: Método que comprueba el valor del tipo introducido.
        '''
        if not isinstance(tipo, str):
            raise Exception("Se esperaba un objeto de tipo str como valor de entrada.")
        if not (tipo=='real' or tipo=='virtual'):
            raise Exception("Tipo solo admite dos valores: real o virtual.")
        
        
        
    def Intersectar(self,tipo='real'):
        '''!
        @brief: Método que cálcula la intersección entre las dos líneas.
        @param tipo str: opción que permite establecer si las intersecciones calculadas son reales o virtuales.
        @note tipo: Valores validos: real,virtual 
        '''
        self.__checkTipo(tipo)
        #Coordenadas de cada punto.
        xi1=self.__l1.getPuntoInicial().getX()
        yi1=self.__l1.getPuntoInicial().getY()
        zi1=self.__l1.getPuntoInicial().getZ()
        
        xf1=self.__l1.getPuntoFinal().getX()
        yf1=self.__l1.getPuntoFinal().getY()
        zf1=self.__l1.getPuntoFinal().getZ()
        
        xi2=self.__l2.getPuntoInicial().getX()
        yi2=self.__l2.getPuntoInicial().getY()
        zi2=self.__l2.getPuntoInicial().getZ()
        
        xf2=self.__l2.getPuntoFinal().getX()
        yf2=self.__l2.getPuntoFinal().getY()
        zf2=self.__l2.getPuntoFinal().getZ()
        
        v1=[xf1-xi1,yf1-yi1,zf1-zi1]
        v2=[xf2-xi2,yf2-yi2,zf2-zi2]
        A=matrix([[xf2-xf1,v1[0],v2[0]],
                 [yf2-yf1,v1[1],v2[1]],
                 [zf2-zf1,v1[2],v2[2]]])
        
        if det(A)==0:
            #print(v1,v2)

            A=matrix([[v1[1],-v1[0],0],
                      [0,v1[2],-v1[1]],
                      [v2[1],-v2[0],0],
                      [0,v2[2],-v2[1]]])
            
            B=array([xf1*v1[1]-yf1*v1[0],yf1*v1[2]-zf1*v1[1],xf2*v2[1]-yf2*v2[0],yf2*v2[2]-zf2*v2[1]])
            sal=lstsq(A,B)
            print(sal)
            x=float(sal[0][0])
            y=float(sal[0][1])
            z=float(sal[0][2])
            
            if tipo=='real':
                #intervalos de definicion.
                ixi=sorted([xi1,xf1])
                iyi=sorted([yi1,yf1])
                izi=sorted([zi1,zf1])
                
                ixf=sorted([xi2,xf2])
                iyf=sorted([yi2,yf2])
                izf=sorted([zi2,zf2])
                
                if x>=min(ixi) and x<=max(ixi) \
                and y>=min(iyi) and y<=max(iyi) \
                and z>=min(izi) and z<=max(izi) \
                and x>=min(ixf) and x<=max(ixf) \
                and y>=min(iyf) and y<=max(iyf) \
                and z>=min(izf) and z<=max(izf):
                    return pt3.Punto3D(x,y,z)
                
                
            elif tipo=='virtual':
                return pt3.Punto3D(x,y,z)
            
        else:
            return None
        
        
        
        
def main():

    la=l3d.Linea3D(pt3.Punto3D(0.0,0.0,0.0),pt3.Punto3D(10,10,10))
    lb=l3d.Linea3D(pt3.Punto3D(30,30,30),pt3.Punto3D(40,40,40))
    i1=Interseccion3D(la,lb)
    i2=Interseccion3D(lb,la)
    sal=i1.Intersectar(tipo='real')
    if sal==None:
        print(sal)
    else:
        print(sal.getX(),sal.getY(),sal.getZ())
    #print(sal.getX(),sal.getY())
    la=l3d.Linea3D(pt3.Punto3D(0.0,0.0,50.0),pt3.Punto3D(10,0,50))
    lb=l3d.Linea3D(pt3.Punto3D(20,50,50),pt3.Punto3D(40,30,50))
    i1=Interseccion3D(la,lb)
    sal=i1.Intersectar(tipo='virtual')
    if sal==None:
        print(sal)
    else:
        print(sal.getX(),sal.getY(),sal.getZ())
    
    
if __name__=="__main__":
    main()
        
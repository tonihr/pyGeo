#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 9/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2011 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.Punto2D as pt2
import Geometrias.Punto3D as pt3
import Geometrias.Angulo as ang
from math import sin,cos

class Radiacion2D(object):
    '''!
    classdocs
    '''
    __x=None
    __y=None
    __d=None
    __az=None


    def __init__(self, PuntoEstacion,Distancia,Azimut):
        '''!
        Constructor
        '''
        self.setPuntoEstacion(PuntoEstacion)
        self.setDistancia(Distancia)
        self.setAzimut(Azimut)
        
        
    def setPuntoEstacion(self,PuntoEstacion):
        '''!
        @brief: Método que establece el Punto estación.
        @param PuntoEstacion Punto2D|Punto3D: Punto estación con las coordenadas.
        '''
        if isinstance(PuntoEstacion, pt2.Punto2D):
            self.__x=PuntoEstacion.getX()
            self.__y=PuntoEstacion.getY()
        elif isinstance(PuntoEstacion, pt3.Punto3D):
            self.__x=PuntoEstacion.getX()
            self.__y=PuntoEstacion.getY()
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D o Punto3D como valor de entrada.")
        
    def setDistancia(self,Distancia):
        '''!
        @brief: Método que asigna y comprueba la distancia introducida.
        @param Distancia float|int|str: Distancia de cálculo.
        '''
        if isinstance(Distancia, float) or isinstance(Distancia, int) or isinstance(Distancia, str):
            try:
                float(Distancia)
            except Exception as e:
                raise Exception(e)
            finally:
                self.__d=float(Distancia)
        else:
            raise Exception("Valor de distancia no válido.")
        
    def setAzimut(self,Azimut):
        '''!
        @brief: Método que asigna y comprueba el azimut introducido.
        @param Distancia float|int|str|Angulo: Distancia de cálculo.
        '''
        if isinstance(Azimut, float) or isinstance(Azimut, int) or isinstance(Azimut, str):
            try:
                float(Azimut)
                ang.Angulo(Azimut,formato='centesimal')
            except Exception as e:
                raise Exception(e)
            finally:
                a1=ang.Angulo(Azimut,formato='centesimal')
                a1.Convertir('radian')
                self.__az=float(a1.getAngulo())
        elif isinstance(Azimut, ang.Angulo):
            if Azimut.getFormato()=='centesimal':
                Azimut.Convertir('radian')
                self.__az=Azimut.getAngulo()
            else:
                raise Exception("Se esperaba un ángulo de entrada de tipo centesimal.")
        else:
            raise Exception("Valor de azimut no válido.")
        
    def Radiacion2D(self):
        '''!
        @brief: Método que cálculo la radiación con los parametros introducidos.
        @return Punto2D: Devuelve un Punto2D con las coordenadas del punto radiado.
        '''
        xs=self.__x+(self.__d*sin(self.__az))
        ys=self.__y+(self.__d*cos(self.__az))
        return pt2.Punto2D(xs,ys)
        
        
        
        
def main():
    rad=Radiacion2D(pt2.Punto2D(10,20),40,ang.Angulo(56245,formato='centesimal'))
    #rad=Radiacion2D(pt2.Punto2D(10,20),40,50)
    sal=rad.Radiacion2D()
    print(sal.getX(),sal.getY())       
        
if __name__=="__main__":
    main()

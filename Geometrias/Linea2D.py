#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 1/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import sys
sys.path.append('..')
from Geometrias.Punto2D import Punto2D

class Linea2D(object):
    '''!
    Clase destinada a almacenar la información de una línea bidimensional.
    Ejemplos de declaración del un objeto de la clase:\n
    l=Linea2D()-->Constructor vacío.\n
    l=Linea2D(Punto2D(10,10),Punto2D(20,20))
    '''
    __pini=None
    __pfin=None


    def __init__(self, *args):
        '''!
        Constructor de la clase Linea2D.
        @param args1 Punto2D: Punto inicial de la linea.
        @param args2 Punto2D: Punto final de la línea.
        @exception: Se producira una excepción si se introducen más o menos argumentos de los admitidos por la clase.
        '''
        if len(args)==0:
            pass
        elif len(args)==2:
            self.setPuntoInicial(args[0])
            self.setPuntoFinal(args[1])
            self.__checkLinea()
        else:
            raise Exception("La clase Linea2D recibe 2 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
        
    def setPuntoInicial(self,PuntoInicial):
        '''!
        @brief: Método para introducir o modificar el punto inicial de la linea.
        @param PuntoInicial Punto2D: Punto inicial de la línea.
        @exception: Se producira una excepción si no se introduce un objeto de la clase Punto2D como valor de entrada del método.
        '''
        if isinstance(PuntoInicial, Punto2D):
            self.__pini=PuntoInicial
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D.")
        if self.__pini!=None and self.__pfin!=None:
            self.__checkLinea()
        
    def setPuntoFinal(self,PuntoFinal):
        '''!
        @brief: Método para introducir o modificar el punto final de la linea.
        @param PuntoFinal Punto2D: Punto final de la línea.
        @exception: Se producira una excepción si no se introduce un objeto de la clase Punto2D como valor de entrada del método.
        '''
        if isinstance(PuntoFinal, Punto2D):
            self.__pfin=PuntoFinal
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D.")
        if self.__pini!=None and self.__pfin!=None:
            self.__checkLinea()
        
    def __checkLinea(self):
        '''!
        @brief: Método para comprobar que el punto inicial y final de la línea son distintos.
        '''
        x1=self.__pini.getX()
        y1=self.__pini.getY()
        x2=self.__pfin.getX()
        y2=self.__pfin.getY()
        
        if x1==x2 and y1==y2:
            raise Exception("El punto inicial y final de la linea deben de ser distintos.")
        
    def getPuntoInicial(self):
        '''!
        @brief: Método que devuelve el Puno inicial de la línea.
        @return Punto2D: Punto inicial. 
        '''
        return self.__pini
    
    def getPuntoFinal(self):
        '''!
        @brief: Método que devuelve el Puno final de la línea.
        @return Punto2D: Punto final. 
        '''
        return self.__pfin
    
    def getAX(self):
        '''!
        @brief: Método que devuelve el incremento de coordenadas en el eje X de la línea.
        @return float: Incremento X. 
        '''
        x1=self.__pini.getX()
        x2=self.__pfin.getX()
        return x2-x1
    
    def getAY(self):
        '''!
        @brief: Método que devuelve el incremento de coordenadas en el eje Y de la línea.
        @return float: Incremento Y. 
        '''
        y1=self.__pini.getY()
        y2=self.__pfin.getY()
        return y2-y1
    
    def getDisnatcia(self):
        '''!
        @brief: Método que devuelve la distancia de la línea.
        @return float: Distancia. 
        '''
        import Topografia.Distancia2D
        d=Topografia.Distancia2D.Distancia2D(self.__pini,self.__pfin)
        return d.getDistancia2D()
    
    def getAzimut(self):
        '''!
        @brief: Devuleve el aximut de la linea.
        @return float: Azimut.
        '''
        import Topografia.Azimut
        az=Topografia.Azimut.Azimut(self.__pini,self.__pfin)
        return az.getAzimut()
    
    def toString(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato str.
        @return str: Un string con toda la información de la linea.
        '''
        return "Punto Inicial: X: "+str(self.__pini.getX())+" Y: "+str(self.__pini.getY())+"\n"\
            "Punto Final: X: "+str(self.__pfin.getX())+" Y: "+str(self.__pfin.getY())+"\n"\
            "AX: "+str(self.getAX())+"\n"\
            "AY: " +str(self.getAX())+"\n"\
            "Dintancia: "+str(self.getDisnatcia())+"\n"\
            "Azimut: "+str(self.getAzimut())
            
    def toJSON(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato JSON.
        @return str: Un string en formato JSON.
        '''
        return "{\n"+\
            '"Punto inicial":'+"\n" +self.__pini.toJSON()+","+"\n"\
            '"Punto final":'+"\n" +self.__pfin.toJSON()+","+"\n"\
            '"AX":'+'"'+str(self.getAX())+'"'+",\n"\
            '"AY":'+'"'+str(self.getAY())+'"'+",\n"\
            '"Distancia":'+'"'+str(self.getDisnatcia())+'"'+",\n"\
            '"Azimut":'+'"'+str(self.getAzimut())+'"'+"\n"\
            +"}"
            
            
    def toGeoJSON(self):
        '''!
        @brief: Método que devuleve un GeoJSON del punto.
        @return str: Un string en formato JSON.
        '''
        
        return "{\n"+\
            '"type":"LineString"'+",\n"\
            '"coordinates":'+\
            '['+\
            '['+\
            str(self.__pini.getX())+','+str(self.__pini.getY())+'],'+\
            '['+\
            str(self.__pfin.getX())+','+str(self.__pfin.getY())+']]'+"\n"\
            "}"
            
def main():
    l=Linea2D(Punto2D(10,10),Punto2D(20,30))
    print(l.toString())
    print(l.toJSON())
    import json
    print(json.loads(l.toJSON())['Punto inicial']['X'])
    print(json.loads(l.toGeoJSON())['coordinates'])
        
        
        
if __name__=="__main__":
    main()
    
    
        
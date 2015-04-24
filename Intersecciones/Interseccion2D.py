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
import Geometrias.Linea2D as l2d
import Geometrias.Punto2D as pt2
from numpy import matrix,array,add,greater_equal
from numpy.linalg import det,solve


class Interseccion2D(object):
    '''!
    classdocs
    '''
    __l1=None
    __l2=None


    def __init__(self, Linea2D1,Linea2D2):
        '''!
        Constructor de la clase Interseccion2D.
        '''
        self.__checkFirstLine(Linea2D1)
        self.setFirstLine(Linea2D1)
        self.__checkSecondLine(Linea2D2)
        self.setSecondLine(Linea2D2)
        
        
    def __checkFirstLine(self,Linea2D1):
        '''!
        @brief: Método que comprueba la primera línea introducida.
        @param Linea2D1 Linea2D: Objeto de la clase Linea2D.
        '''
        
        if not isinstance(Linea2D1, l2d.Linea2D):
            raise Exception("Se esperaba un objeto de la clase Linea2D como primer valor de entrada.")
        
    def __checkSecondLine(self,Linea2D2):
        '''!
        @brief: Método que comprueba la primera línea introducida.
        @param Linea2D1 Linea2D: Objeto de la clase Linea2D.
        '''
        
        if not isinstance(Linea2D2, l2d.Linea2D):
            raise Exception("Se esperaba un objeto de la clase Linea2D como segundo valor de entrada.")
        
    def setFirstLine(self,Linea2D1):
        '''!
        @brief: Método para introducir la primera línea de cálculo.
        @param Linea2D1 Linea2D: Objeto de la clase Linea2D.
        '''
        self.__l1=Linea2D1
        
    def setSecondLine(self,Linea2D2):
        '''!
        @brief: Método para introducir la primera línea de cálculo.
        @param Linea2D1 Linea2D: Objeto de la clase Linea2D.
        '''
        self.__l2=Linea2D2
        
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
        
        xf1=self.__l1.getPuntoFinal().getX()
        yf1=self.__l1.getPuntoFinal().getY()
        
        xi2=self.__l2.getPuntoInicial().getX()
        yi2=self.__l2.getPuntoInicial().getY()
        
        xf2=self.__l2.getPuntoFinal().getX()
        yf2=self.__l2.getPuntoFinal().getY()
        
        v1=[xf1-xi1,yf1-yi1]
        v2=[xf2-xi2,yf2-yi2]
        A=matrix([[v1[1],-v1[0]],
                  [v2[1],-v2[0]]])
        B=array([xf1*v1[1]-yf1*v1[0],xf2*v2[1]-yf2*v2[0]])
        #print(A,B)
        if det(A)==0:
            A=add.reduce(A, 0)
            B=add.reduce(B, 0)
            #print(A,B)
            if B==0:
                # sol ay=bx
                return None
            if B!=0:
                if A.item((0, 0))==0:
                    x=xi1
                    y=B/A.item((0, 1))
                elif A.item((0, 1))==0:
                    x=B/A.item((0, 0))
                    y=yi1
        else:
            sol=solve(A,B)
            x=sol[0]
            y=sol[1]
            #print(x,y)
        #Cálculo de la interseccion #y=ax+b
#         a1=None
#         a2=None
#         b1=None
#         b2=None
#             
#         if abs(yf1-yi1)==0.0:
#             a1=0.0
#         elif abs(xf1-xi1)==0.0:
#             a1=None
#         else:
#             a1=(yf1-yi1)/(xf1-xi1)
#             
#         if abs(yf2-yi2)==0.0:
#             a2=0.0
#         elif abs(xf2-xi2)==0.0:
#             a2=None
#         else:
#             a2=(yf2-yi2)/(xf2-xi2)
#             
#         if a1==None:
#             b1=xi1
#         else:
#             b1=yi1-a1*xi1
#             
#         if a2==None:
#             b2=xi2
#         else:
#             b2=yi2-a2*xi2
#         
#             
# #         print(a1,a2,b1,b2)
#         if a1==None and a2==None:
#             #Paralelas.
#             return None
#         elif a1==None and a2==0.0:
#             x=xi2
#             y=a2
#             
#         elif a1==0.0 and a2==None:
#             x=b2
#             y=b1
#         elif a1==None:
#             x=b1
#             y=(b2-b1)/(-a2)
#         elif a2==None:
#             x=b2
#             y=(b2-b1)/(a1)
#         elif a1==None and a2==None:
#             x=(b2-b1)
#         else:
#             try:
#                 x=(b2-b1)/(a1-a2)
#                 y=a1*x+b1
#             except:
#                 x=0.0
#                 y=a1*x+b1
                
                
        if tipo=='real':
            #intervalos de definicion.
#             ixi=sorted([xi1,xf1])
#             iyi=sorted([yi1,yf1])
#             ixf=sorted([xi2,xf2])
#             iyf=sorted([yi2,yf2])
#             print(ixi,iyi,ixf,iyf)
#             print(str(round(y,20)))
#             print(round(min(iyi),20))
#             print(y==min(iyi))
#             print(self.__l1.PointIn(pt2.Punto2D(x,y),tolerance=0.001))
#             print(self.__l2.PointIn(pt2.Punto2D(x,y),tolerance=0.001))
#             print(x>=min(ixi),x<=max(ixi),y>=min(iyi),y<=max(iyi),x>=min(ixf),x<=max(ixf),y>=min(iyf),y<=max(iyf))
#             print(greater_equal([x],[min(ixi),min(ixf)]))
#             print(greater_equal([y],[min(iyi),min(iyf)]))
#             print(y,min(iyf))
#             if x>=min(ixi) and x<=max(ixi) and y>=min(iyi) and y<=max(iyi) and x>=min(ixf) and x<=max(ixf) and y>=min(iyf) and y<=max(iyf):
#             if greater_equal([x,min(ixi)],[y,min(iyi)],[x,min(ixf)],[y,min(iyf)]):
            if self.__l1.PointIn(pt2.Punto2D(x,y),tolerance=0.001) and self.__l1.PointIn(pt2.Punto2D(x,y),tolerance=0.001):
                return pt2.Punto2D(x,y)
            else: 
                return None
        elif tipo=='virtual':
            return pt2.Punto2D(x,y)
            
        
        
        
        
def main():
#     la=l2d.Linea2D(pt2.Punto2D(0.0,0.0),pt2.Punto2D(0,10))
#     lb=l2d.Linea2D(pt2.Punto2D(0,5),pt2.Punto2D(20,0))
#     i1=Interseccion2D(la,lb)
#     sal=i1.Intersectar(tipo='real')
#     if sal==None:
#         print(sal)
#     else:
#         print(sal.getX(),sal.getY())
#         
#         
#     la=l2d.Linea2D(pt2.Punto2D(0.0,0.0),pt2.Punto2D(10,10))
#     lb=l2d.Linea2D(pt2.Punto2D(10,10),pt2.Punto2D(20,20))
#     i1=Interseccion2D(la,lb)
#     sal=i1.Intersectar(tipo='real')
#     if sal==None:
#         print(sal)
#     else:
#         print(sal.getX(),sal.getY())
# 
#     la=l2d.Linea2D(pt2.Punto2D(0.0,0.0),pt2.Punto2D(10,10))
#     lb=l2d.Linea2D(pt2.Punto2D(0.0,10),pt2.Punto2D(0.0,-5))
#     i1=Interseccion2D(la,lb)
#     sal=i1.Intersectar(tipo='real')
#     print(sal.getX(),sal.getY())
#     
#     la=l2d.Linea2D(pt2.Punto2D(0.0,0.0),pt2.Punto2D(10,0))
#     lb=l2d.Linea2D(pt2.Punto2D(20,50),pt2.Punto2D(40,30))
#     i1=Interseccion2D(la,lb)
#     sal=i1.Intersectar(tipo='virtual')
#     if sal==None:
#         print(sal)
#     else:
#         print(sal.getX(),sal.getY())
        
        
    la=l2d.Linea2D(pt2.Punto2D(3.4,39.6),pt2.Punto2D(3.4,14))
    lb=l2d.Linea2D(pt2.Punto2D(18,37),pt2.Punto2D(3.4,37))
    i1=Interseccion2D(la,lb)
    sal=i1.Intersectar(tipo='real')
    if sal==None:
        print(sal)
    else:
        print(sal.getX(),sal.getY())
    
    
    
if __name__=="__main__":
    main()
        
        
        
        
        
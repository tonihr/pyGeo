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

import Geometrias.Poligono2D as pol2d
import Geometrias.PoliLinea2D as poli2d
import Geometrias.Punto2D as pt2d
import Geometrias.Linea2D as lin2d
import Intersecciones.Interseccion2D as inter2d

class PointInPolygon(object):
    '''
    classdocs
    '''
    __pol=None
    __pt=None
    __bbox=None
    __lins=None

    def __init__(self, *args):
        '''
        Constructor
        '''
        if len(args)==0:
            pass
        elif len(args)==2:
            self.setPoligono(args[0])
            self.setPunto(args[1])
        else:
            raise Exception("La clase PointInPolygon recibe 2 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
            
        
    def setPoligono(self,Poligono2D):
        '''!
        '''
        self.__bbox=None
        self.__lins=None
        if isinstance(Poligono2D, pol2d.Poligono2D):
            self.__pol=Poligono2D
        elif isinstance(Poligono2D, poli2d.PoliLinea2D):
            poligono=pol2d.Poligono2D(Poligono2D)
            self.__pol=poligono
            poligono=None
        else:
            raise Exception("Se esperaba un objeto de la clase Poligono2D.")
        self.__bbox=self.__pol.getBbox()
        self.__lins=self.__pol.getPolilinea2D().getLineas()
        print(self.__bbox[0].getX(),self.__bbox[0].getY(),self.__bbox[1].getX(),self.__bbox[1].getY())
        
    def setPunto(self,Punto2D):
        '''!
        '''
        self.__pt=None
        if isinstance(Punto2D, pt2d.Punto2D):
            self.__pt=Punto2D
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D.")
        
    def Dentro(self):
        '''!
        '''
        # Comprobar si el Punto esta dentro de bbox del Poligono2D.
        pto=pt2d.Punto2D()
        if (self.__pt.getX()<self.__bbox[0].getX() or self.__pt.getX()>self.__bbox[1].getX()) and (self.__pt.getY()>self.__bbox[0].getY() or self.__pt.getY()<self.__bbox[1].getY()):
            return False        
        else:
            #Comprobar si el punto está sobre una linea del poligono.
            for i in self.__lins:
                if i.PointIn(self.__pt)==True:
                    return False
#                     return 'Perimetro'


            lin=None
            Rmatch=0
            #Right intersection.
            pto.setX(self.__bbox[1].getX())
            pto.setY(self.__pt.getY())
            #pt=pt2d.Punto2D(self.__bbox[1].getX(),self.__pt.getY())
            lin=lin2d.Linea2D(self.__pt,pto)
            print(lin.getPuntoInicial().getX(),lin.getPuntoInicial().getY())
            print(lin.getPuntoFinal().getX(),lin.getPuntoFinal().getY())
            for i in self.__lins:
                Intersecta=inter2d.Interseccion2D(lin,i)
                res=Intersecta.Intersectar(tipo='real')
                if res!=None:
                    print(res.getX(),res.getY())
                    if i.getPuntoInicial().getY()==res.getY() and Rmatch%2!=0:
                        continue
                    elif i.getPuntoInicial().getY()==res.getY() and Rmatch%2==0:
                        Rmatch+=1
                        continue
                    elif i.getPuntoFinal().getY()==res.getY() and Rmatch%2!=0:
                        continue
                    elif i.getPuntoFinal().getY()==res.getY() and Rmatch%2==0:
                        Rmatch+=1
                        continue
                    Rmatch+=1
                    
                    
            pto.setX(self.__bbox[0].getX())
            lin.setPuntoFinal(pto)
            Lmatch=0
            #Left Intersection
            #lin=lin2d.Linea2D(self.__pt,pt2d.Punto2D(self.__bbox[0].getX(),self.__pt.getY()))
            print(lin.getPuntoInicial().getX(),lin.getPuntoInicial().getY())
            print(lin.getPuntoFinal().getX(),lin.getPuntoFinal().getY())
            for i in self.__lins:
                #Intersecta=None
                Intersecta=inter2d.Interseccion2D(lin,i)
                res=Intersecta.Intersectar(tipo='real')
                print(res)
                if res!=None:
                    print(res.getX(),res.getY())
                    print(i.getPuntoInicial().getY(),i.getPuntoFinal().getY(),res.getY())
#                     if i.getPuntoInicial().getY()==i.getPuntoFinal().getY()==res.getY() and Lmatch%2!=0:
#                         continue
#                     elif i.getPuntoInicial().getY()==i.getPuntoFinal().getY()==res.getY() and Lmatch%2==0:
#                         Lmatch+=1
#                         continue
                    if i.getPuntoInicial().getY()==res.getY() and Lmatch%2!=0:
                        continue
                    elif i.getPuntoInicial().getY()==res.getY() and Lmatch%2==0:
                        Lmatch+=1
                        continue
                    elif i.getPuntoFinal().getY()==res.getY() and Lmatch%2!=0:
                        continue
                    elif i.getPuntoFinal().getY()==res.getY() and Lmatch%2==0:
                        Lmatch+=1
                        continue
                    Lmatch+=1
                    
            print(Lmatch,Rmatch)
            
            if Rmatch==0 and Lmatch==0:
                return False
            elif Rmatch%2==0 and (Lmatch%2!=0 or Lmatch==1):
                return False
            elif Lmatch%2==0 and (Rmatch%2!=0 or Rmatch==1):
                return False
            elif Lmatch%2!=0 and Rmatch%2!=0:
                return True
                    
def main():
    
    pol=pol2d.Poligono2D()
    pol.setFromWKT('POLYGON (3.4 39.6, 40 39.6, 40 14, 3.4 14, 3.4 39.6)')
    
    punto=pt2d.Punto2D(18,37)
    
    PIP=PointInPolygon(pol,punto)
    print(PIP.Dentro())


    pass

if __name__=='__main__':
    main()
        
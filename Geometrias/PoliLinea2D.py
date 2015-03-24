'''
Created on 14/3/2015

@author: toni
'''
import Geometrias.Punto2D as pt2
import Geometrias.Linea2D as l2d
import Intersecciones.Interseccion2D as inter2d

class PoliLinea2D(object):
    '''
    classdocs
    '''
    __ptos=[]
    __lins=[]


    def __init__(self):
        '''
        Constructor
        '''
        
        
        
    def setPoliLineaFromPuntos(self,Puntos):
        '''!
        '''
        if isinstance(Puntos, list):
            for i in Puntos:
                if not isinstance(i, pt2.Punto2D):
                    raise Exception("Uno de los elementos de la lista no es un objeto de la clase Punto2D.")
                else:
                    self.__ptos.append(i)
            for indi,i in enumerate(Puntos):
                if indi==len(Puntos):
                    break
                else:
                    pt1=i
                    pt2=Puntos[indi+1]
                    l=l2d.Linea2D(pt1,pt2)
                    self.__lins.append(l)      
        else:
            raise Exception("Se esperaba una lista como argumento de entrada del método.")
        self.__checkPoli()
        
    
    
    def setPoliLineaFromLineas(self,Lineas):
        '''!
        '''
        if isinstance(Lineas, list):
            for i in Lineas:
                if not isinstance(i, l2d.Linea2D):
                    raise Exception("Uno de los elementos de la lista no es un objeto de la clase Linea2D.")
                else:
                    self.__lins.append(i)            
        else:
            raise Exception("Se esperaba una lista como argumento de entrada del método.")
        self.__checkPoli()
        
    def __checkPoli(self):
        '''
        '''
        for indi,i in enumerate(self.__lins):
            if indi==len(self.__lins)-1:
                break
            else:
                l1=i
                l2=self.__lins[indi+1]
                p1=l1.getPuntoFinal()
                p2=l2.getPuntoInicial()
                if p1.getX()==p2.getX() and p1.getY()==p2.getY():
                    pass
                else:
                    raise Exception("La polilinea no es continua.")
                
    def isClose(self):
        '''
        '''
        l1=self.__lins[-1]
        l2=self.__lins[0]
        p1=l1.getPuntoFinal()
        p2=l2.getPuntoInicial()
        if p1.getX()==p2.getX() and p1.getY()==p2.getY():
            return True
        else:
            return False
        
    def selfIntersect(self):
        '''
        '''
        Sal=[]
        for indi1,i in enumerate(self.__lins):
            for indi2,j in enumerate(self.__lins):
                if indi1==indi2 or indi1>indi2:
                    continue
                elif indi1+1==indi2:
                    continue
                elif indi1-1==indi2:
                    continue
                elif self.isClose()==True:
                    if indi1==len(self.__lins)-1 and indi2==0:
                        continue
                    if indi2==len(self.__lins)-1 and indi1==0:
                        continue
                else:
                    inter=inter2d.Interseccion2D(i,j)
                    sal=inter.Intersectar(tipo='real')
                    if sal==None:
                        continue
                    else:
                        print(indi1,indi2,sal.getX(),sal.getY())
        
        
        
        
def main():
    pl=PoliLinea2D()
    pl.setPoliLineaFromLineas([l2d.Linea2D(pt2.Punto2D(0.0,0.0),pt2.Punto2D(10,0)),
                               l2d.Linea2D(pt2.Punto2D(10.0,0),pt2.Punto2D(-10,10)),
                               l2d.Linea2D(pt2.Punto2D(-10,10.0),pt2.Punto2D(10,10)),
                               l2d.Linea2D(pt2.Punto2D(10.0,10.0),pt2.Punto2D(-10,0)),
                               l2d.Linea2D(pt2.Punto2D(-10.0,0),pt2.Punto2D(0,0))])
    print(pl.isClose())
    print(pl.selfIntersect())
    pass

if __name__=='__main__':
    main()

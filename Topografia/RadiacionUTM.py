#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 4/5/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2014 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.PuntoUTM as putm
import Geometrias.Angulo as ang
import Topografia.Azimut as azi





import Geometrias.Punto2D as pt2d
import Topografia.Radiacion2D as rad2d
import Proyecciones.UTM2Geo as utm2geo
import Geodesia.RadiosDeCurvatura as radCur
import Geodesia.Elipsoides as elip
from math import cos,pi
from numpy import mean


class RadiacionUTM(rad2d.Radiacion2D):
    '''
    classdocs
    '''

    def __init__(self, PuntoEstacion,Referencias=[],Lecturas=[]):
        '''
        Constructor de la clase RadiacionUTM.
        '''
        rad2d.Radiacion2D.__init__(self,PuntoEstacion,Referencias,Lecturas)
        
    def setPuntoEstacion(self, PuntoEstacion):
        if isinstance(PuntoEstacion, putm.PuntoUTM):
            self.__pEst=PuntoEstacion
        else:
            raise Exception("No es un puntoUTM")
        #rad2d.Radiacion2D.setPuntoEstacion(self, PuntoEstacion)
        
    def __checkRefLec(self):
        '''!
        '''
        if self.getReferencias()==[]:
            return
        if self.getLecturasReferencias()==[]:
            return
        if len(self.getReferencias())==len(self.getLecturasReferencias()):
            return
        else:
            raise Exception('El número de lecturas no coincide con el número de referencias introducidas.')
        
    def RadiacionUTM(self,Elipsoide,Distancia,LecturaHorizontal):
        '''!
        @brief: Método que cálculo la radiación con los parametros introducidos.
        @return Punto2D: Devuelve un Punto2D con las coordenadas del punto radiado.
        '''
        #TO-DO: Se puede introducir la distancia y lectura como listas y hacer bucle de radiación.
        #Comprobaciones.
        try:
            Distancia=float(Distancia)
        except Exception as e:
            raise Exception(e)
        
        if isinstance(LecturaHorizontal, ang.Angulo):
            if not LecturaHorizontal.getFormato()=='centesimal':
                raise Exception('El ángulo debe ser de tipo centesimal.')
        else:
            raise Exception("No es ángulo")
        
        #Claculo de la raidiación.
        desmean=0
        angaux=ang.Angulo()
        angaux.setGirar(True)
        angaux.setNegativos(False)
        self.__checkRefLec()
        
        if self.getReferencias()!=[] and self.getLecturasReferencias()!=[]:
            #Cálculo azimuts referencia.
            azRef=[]
            azimuts=azi.Azimut()
            azimuts.setPuntoInicial(self.__pEst)
            for i in self.__referencias:
                azimuts.setPuntoFinal(i)
                azRef.append(azimuts.getAzimut())
            #print(azRef)
            #Cálculo desorientaciones.
            des=[]
            for i,j in zip(azRef,self.__lecturasRef):
                j.Convertir('radian')
                deso=i-j.getAngulo()
                angaux.setAngulo(deso)
                angaux.setFormato('radian')
                des.append(angaux.getAngulo())
            #print(des)
            #Cálculo de la radiación
            desmean=mean(des)
            
        #1º Radiación aplicando convA k1a, datosdel punto estación y referencia.
        
        
        
        
    
#     def RadiaUTM(self,Elipsoide):
#         '''!
#         '''
#         rc=radCur.RadiosDeCurvatura(Elipsoide)
#         EL=elip.Elipsoides(Elipsoide)
#         #Radiacion con k1a y convergencia A.
#         #Comprobar la escala local.
#         geo1=utm2geo.UTM2Geo(self.__pEst,Elipsoide)
#         nhu1=rc.getRadioPrimerVertical(geo1.getLatitud())
#         ro1=rc.getRadioElipseMeridiana(geo1.getLatitud())
#         k1a=self.__pEst.getEscalaLocalPunto()
#         convA=self.__pEst.getConvergenciaMeridianos()
#         convA=ang.Angulo(convA,formato='pseudosexagesimal')
#         convA.Convertir(Formato='radian')
#         convA=convA.getAngulo()
#         print(k1a,convA)
#         
#         Radia2d=rad2d.Radiacion2D(pt2d.Punto2D(self.__x,self.__y),self.__d*k1a,(self.__az+convA)*200/pi)
#         res=Radia2d.Radiacion2D()
#         
#         putmb=putm.PuntoUTM(res.getX(),res.getY())
#         self.__xsal=res.getX()
#         self.__ysal=res.getY()
#         print(self.__xsal,self.__ysal)
#         xant=0
#         yant=0
#         while(abs(xant-self.__xsal)>0.0001):
#             print(abs(xant-self.__xsal))
#             xant=self.__xsal
#             yant=self.__ysal
#             geo2=utm2geo.UTM2Geo(putmb,Elipsoide)
#             nhu2=rc.getRadioPrimerVertical(geo2.getLatitud())
#             ro2=rc.getRadioElipseMeridiana(geo2.getLatitud())
#             k1b=putmb.getEscalaLocalPunto()
#             convB=putmb.getConvergenciaMeridianos()
#             convB=ang.Angulo(convB,formato='pseudosexagesimal')
#             convB.Convertir(Formato='radian')
#             convB=convB.getAngulo()
#             
#             k1m=(k1a+k1b)/2
#             k1=6/((1/k1a)+(4/k1m)+(1/k1b))
#             s=k1*self.__d
#             azcg=self.__az+convA
#             lat=ang.Angulo(geo1.getLatitud(),formato='pseudosexagesimal')
#             lat.Convertir(Formato='radian')
#             lat=lat.getAngulo()     
#             e2=EL.getSegundaExcentricidad()
#             n2=((e2**2))*(cos(lat)**2) #Probar con la laitud media de ambos.
#             #Coordenada al meridiano.
#             x1=(self.__x-500000)/0.9996
#             x2=(self.__xsal-500000)/0.9996
#             
#             dtAB=(((self.__ysal/0.9996-self.__y/0.9996)*(2*x2+x1))/(6*((nhu1+nhu2)/2)*((ro1+ro2)/2)))*(1+n2)
#             azcc=azcg+dtAB
#             
#             d=s-((1/24)*(((((x1+x2)/2)*(cos(azcc)))/((0.9996**2)*((nhu1+nhu2)/2)*((ro1+ro2)/2)))**2)*s**3)
#             print(dtAB,d)
#             Radia2d.setAzimut(azcc*200/pi)
#             Radia2d.setDistancia(d)
#             res=Radia2d.Radiacion2D()
#             self.__xsal=res.getX()
#             self.__ysal=res.getY()
#             putmb=putm.PuntoUTM(res.getX(),res.getY())
#             print(self.__xsal,self.__ysal)
            
        
        
        
        
def main():
    '''!
    '''
    #from math import pi
    p=putm.PuntoUTM(718763.1524,4397605.0467)
    rutm=RadiacionUTM(p)
    rutm.RadiacionUTM('WGS 84',100,ang.Angulo(150,formato='centesimal'))
    
if __name__=='__main__':
    main()
        
        
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from os.path import exists,isfile
from re import search
from numpy import matrix,dot,linalg,shape
from math import sqrt
import GNSS.GLONASSNavigationReader as R_Nav
import GNSS.GPSNavigationReader as G_Nav
import GNSS.RINEXObservationReader as R_Obs
import GNSS.SatPositioning as sp

class GNSSPositioning(object):
    '''
    classdocs
    '''
    __r=None
    __n=None
    __g=None
    __mixed=None
    __sp3=None
    __atx=None


    def __init__(self, RINEXFile, NavigationFiles, SP3File=None,ATXFile=None):
        '''
        Constructor
        @param RINEXFile str:
        @param NavigationFiles str|[]:
        '''
        self.setRINEXFile(RINEXFile)
        self.setNavigatonFiles(NavigationFiles)
        print(self.__r)
        print(self.__n)
        print(self.__g)
        self.setSP3File(SP3File)
        self.setATXFile(ATXFile)
        #De mommento más adelante ver si es necesario añadir más ficheros.GALILEO...
        
        
    def setRINEXFile(self,RINEXFile):
        '''!
        @brief: Comprueba y asigna el fichero Rinex de osevación.
        @param RINEXFile str: Ruta del fichero RINEX de observación.
        '''
        if not type(RINEXFile)==str:
            raise Exception("El fichero introducido no es de tipo str")
        if not exists(RINEXFile):
            raise Exception("No existe")
        if not isfile(RINEXFile):
            raise Exception("No es un archivo")
        if not (RINEXFile.endswith("o") or RINEXFile.endswith("O"))and not search("\d\d",RINEXFile.split(".")[1]):
            raise Exception("Tipo de fichero rinex no válido.")
        self.__r=RINEXFile
        
    def setNavigatonFiles(self,NavigationFiles):
        '''!
        @brief: Comprueba y asigna los ficheros RINEX de navegación.
        @param NavigationFiles str|[]: Ruta de los ficheros RINEX de navegación
        '''
        if type(NavigationFiles)== str:
            NavigationFiles=[NavigationFiles]
        if type(NavigationFiles)== list:
            #Se chequean las diferentes rutas que puedan existir.
            for i in NavigationFiles:
                if not type(i)==str:
                    raise Exception("No es str")
                if not exists(i):
                    raise Exception("No existe")
                if not isfile(i):
                    raise Exception("No es un archivo")
            #Una vez cuequeadas se asignan los ficheros existentes.
            for i in NavigationFiles:
                if(i.endswith("n") or i.endswith("N"))and search("\d\d",i.split(".")[1]):
                    self.__n=i
                    continue
                if(i.endswith("g") or i.endswith("G"))and search("\d\d",i.split(".")[1]):
                    self.__g=i
                    continue
                if(i.endswith("p") or i.endswith("P"))and search("\d\d",i.split(".")[1]):
                    self.__mixed=i
                    continue
                
    def setSP3File(self,SP3File):
        '''!
        @brief: Comprueba y asigna el fichero de efemérides precisas.
        @param SP3File str: Ruta del fichero de efemérides precisas.
        '''
        if SP3File==None:
            return
        if not type(SP3File)==str:
            raise Exception("El fichero introducido no es de tipo str")
        if not exists(SP3File):
            raise Exception("No existe")
        if not isfile(SP3File):
            raise Exception("No es un archivo")
        if not SP3File.endswith("sp3"):
            raise Exception("Tipo de fichero rinex no válido.")
        self.__sp3=SP3File
        
        
    def setATXFile(self,ATXFile):
        '''!
        @brief: Comprueba y asigna el fichero de antenas.
        @param ATXFile str: Ruta del fichero de antenas.
        '''
        if ATXFile==None:
            return
        if not type(ATXFile)==str:
            raise Exception("El fichero introducido no es de tipo str")
        if not exists(ATXFile):
            raise Exception("No existe")
        if not isfile(ATXFile):
            raise Exception("No es un archivo")
        if not ATXFile.endswith("atx"):
            raise Exception("Tipo de fichero de antenas.")
        self.__atx=ATXFile
        
    def PosicionamientoCodigo(self,Observable):
        '''
        @brief: Método que realiza el posicionamiento por código para cada una de las épocas disponibles en el fichero RINEX de observación.
        @param Observable: C o P
        @type Observable: str
    
        @note: Si en una época hay 4 satélites o menos,no se realizara el posicionamiento.
        @note 2: 
        '''
        #Se obtienen los observables de código.
        obs=R_Obs.RINEXObservationReader(self.__r)
        codigo=obs.getObservation([Observable])
        cabecera=obs.getHeader()

        #Se lee el fichero de navegación GPS.
        nav1=G_Nav.GPSNavigationReader(self.__n)
        efem_G=nav1.getNavigation()

        #Se lee el fichero de navegación GLONASS.
        try:
            nav2=R_Nav.GLONASSNavigationReader(self.__g)
            efem_R=nav2.getNavigation()
        except:
            pass
        
        
        #Fechas únicas en el observable de código.
        ##Con estas son las que se realizara el posicionamiento.
        Fechas=[i[0] for i in codigo]
        Fechas=list(set(Fechas))
        Fechas.sort()


        for i in Fechas:
            #Para cada fecha existente en los observables se realizara un posicionamiento.
            #Coger todos los observables disponibles para esa fecha.
            ini=False
            fin=False
            Obs_act=[]
            for j in codigo:
                if j[0]==i:
                    ini=True
                    Obs_act.append(j)
##                    print(j)
                if ini and j[0]!=i:
                    fin=True
                if fin:
                    break
            Obs_act.sort(key=lambda x: x[1])
##            for j in Obs_act:
##                print(j)
##            input()
            #Buscar la efemeride que mejor se adecua al obserbable.
            Efemerides_act=[]
            for j in Obs_act:
                dif=[]  #Diferencias de tiempo.
##                print(j)
                if "G" in j[1] and self.__n!=None:
                    for indi,k in enumerate(efem_G):
                        if k[1]==j[1]:
                            dif.append([j[0]-k[0],indi])
                    util=dif[0]
                    for k in dif:
                        if k[0]<util[0]:
                            util=k
                    Efemerides_act.append(efem_G[util[1]])   
##                    print(util)
##                    print(efem_G[util[1]])
##                    input()
                    continue
                elif "R" in j[1] and self.__g!=None:
                    for indi,k in enumerate(efem_R):
                        if k[1]==j[1]:
                            dif.append([k[0]-j[0],indi])
##                    for t in dif:
##                        print(t)
                            
                    util=dif[0]
                    for k in dif:
                        if k[0]<util[0]:
                            util=k
##                    print(util)
##                    print(util[1])
##                    print(efem_R[util[1]])
##                    for t in efem_R:
##                        print(t)
##                        input()
                    Efemerides_act.append(efem_R[util[1]])
                    continue
                else:
                    continue

##            for j in Efemerides_act:
##                print(j)
##            input()

            #Algoritmo MMCC.
            pos_sat=sp.SatPositioning(Efemerides_act,Obs_act)
            sats=pos_sat.getPosition()

            #Aplicación de MMCC para obterner la posicion del receptor.
            Xest=0
            Yest=0
            Zest=0
            if cabecera["X"]!=0:
                Xest=float(cabecera["X"])
            if cabecera["Y"]!=0:
                Yest=float(cabecera["Y"])
            if cabecera["Z"]!=0:
                Zest=float(cabecera["Z"])
            At0=0
            est=1
            est_ant=0
            c=2.99792458e8
            itera=0
            while(abs(est_ant-est)>1e-7):
                est_ant=est
                A=[]
                K=[]
                A0=None
                K0=None
                for j in sats:
                    ro=sqrt((float(j[2])-Xest)**2+(float(j[3])-Yest)**2+(float(j[4])-Zest)**2)
                    dx=(float(j[2])-Xest)/ro
                    dy=(float(j[3])-Yest)/ro
                    dz=(float(j[4])-Zest)/ro
                    l=j[5]-ro+j[6]*c
##                    l=j[5]-ro+j[6]*c+At0
                    A.append([-dx,-dy,-dz,1])
                    K.append([l])

                A0=matrix(A)
                K0=matrix(K)
                #Ponderación
                sol=linalg.lstsq(A0, K0)

                R=dot(A0,sol[0])-K0
##                print(R) 

                val=dot(R.transpose(),R)
                gdl=shape(A0)
                est=sqrt(val/(gdl[0]-gdl[1]))

                Ax=float(sol[0][0])
                Ay=float(sol[0][1])
                Az=float(sol[0][2])
                At=float(sol[0][3])

##                print(Ax,Ay,Az,At)

                Xest+=Ax
                Yest+=Ay
                Zest+=Az
                At0+=At
                itera+=1
            print(Xest,Yest,Zest,est,itera)
            input()
##                print(abs(est_ant-est))
##            input()






def main():
##    pos=GNSS_Positioning('/home/toni/Dropbox/LibGeo/Ejemplos/ALCO272A.14o','/home/toni/Dropbox/LibGeo/Ejemplos/ALCO2720.14n')
    pos=GNSSPositioning('/home/toni/Dropbox/LibGeo/Ejemplos/VCIA2710.14o','/home/toni/Dropbox/LibGeo/Ejemplos/VCIA2710.14n')
#     pos=GNSSPositioning('/home/toni/Dropbox/LibGeo/Ejemplos/VCIA2710.14o',['/home/toni/Dropbox/LibGeo/Ejemplos/VCIA2710.14n','/home/toni/Dropbox/LibGeo/Ejemplos/VCIA2710.14g'])
    
    pos.PosicionamientoCodigo("C1")

if __name__=="__main__":
    main()
        
        
        
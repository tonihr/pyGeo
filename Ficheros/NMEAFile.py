#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 9/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from os.path import isfile,exists,split
from datetime import datetime,timedelta

class NMEAFile(object):
    '''!
    classdocs
    '''
    __filepath=None
    __path=None
    __file=None
    __gga=[]
    __rmc=[]


    def __init__(self, FilePath):
        '''!
        Constructor de la clase NMEA.
        @param FilePath str: Ruta del fichero NMEA.
        '''
        self.__checkFilePath(FilePath)
        f=open(self.__filepath,'r')
        with open(self.__filepath,"r") as f:
            self.__gga=[i for i in f if i.strip()!="" and "$GPGGA" in i and not "#SNAN0" in i]
            f.seek(0)
            self.__rmc=[i for i in f if i.strip()!="" and "$GPRMC" in i and not "#SNAN0" in i]
        f.close()
        
    def __checkFilePath(self,filepath):
        '''!
        '''
        
        if not exists(filepath):
            raise Exception("El archivo introducido no existe")
        if not isfile(filepath):
            raise Exception("El arcivo introducido no es un fichero.")
        self.__filepath=filepath
        self.__path,self.__file=split(filepath)
        
    def getHoras(self):
        '''!
        @brief: Método que devuelve las horas de las épocas de observación.
        @return [str]: Hora de cada observación
        '''
        return [(i.split(",")[1]) for i in self.__gga if i.split(",")[1]!=""]
    
    def getDoys(self):
        '''!
        @brief: Método que transformala fecha dia/mes/año a doy: day of year.
        @return [int]: Doys existentes en el fichero NMEA
        '''
        FechaAUX=[]
        aux=None
        for i in self.__rmc:
            i=i.split(",")[9]
            if aux==i:
                continue
            dia=int(i[0]+i[1])
            mes=int(i[2]+i[3])
            año=int(i[4]+i[5])+2000
            FechaAUX.append(datetime(año, mes, dia, 0, 0, 0).timetuple().tm_yday)
            aux=i
        Fecha=list(set(FechaAUX))
        Fecha.sort(key=int)
        return Fecha
    
    def getFechas(self):
        '''!
        @brief: Método que transformala fecha dia/mes/año a doy: day of year.
        @return [datetime]: Lista de objetos datetime, con los doys existentes en el fichero NMEA.
        '''
        FechaAUX=[]
        aux=None
        for i in self.__rmc:
            i=i.split(",")[9]
            if aux==i:
                continue
            dia=int(i[0]+i[1])
            mes=int(i[2]+i[3])
            año=int(i[4]+i[5])+2000
            FechaAUX.append(datetime(año, mes, dia, 0, 0, 0))
            aux=i
        #Fecha=list(set(FechaAUX))
        return FechaAUX
    
    def getSegundosGPS(self):
        '''!
        @brief: Método que devuelve la hora de cada observacion en segundos de la semana GPS.
        
        @param NombreDia str: Nombre del día de observación. En mayusculas.
        @raise Valor Nombre Dia: Se produce una excepcion en el caso de que el nombre del día no se de tipo String.
        @raise Dia no valido: Se produce una excepcion en el caso de que el dia introducido no sea: LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO.
        @note: si el archivo nmea esta en diferentes intervalos de tiempo 1, 5, 30 segundos la conversión a segundos de la semana GPS funciona bien.
        @return [str]: Lista con los segundos GPS de cada observación.
        '''
        sGPS=[]
        doy_ant=None
        segini=None
        for i in self.__rmc:
            fecha=i.split(",")[9]
            hora=i.split(",")[1]
            dia=int(fecha[0]+fecha[1])
            mes=int(fecha[2]+fecha[3])
            año=int(fecha[4]+fecha[5])+2000
            doy=datetime(año, mes, dia, 0, 0, 0).timetuple().tm_yday
            
            if doy_ant!=doy:
                #print("SI")
                d1=datetime(int(año), 1, 1) + timedelta(int(doy)-1)
                if str(d1.strftime('%A'))== "Monday":
                    segini=86400
                if str(d1.strftime('%A'))== "Tuesday":
                    segini=172800
                if str(d1.strftime('%A'))== "Wednesday":
                    segini=259200
                if str(d1.strftime('%A'))== "Thursday":
                    segini=345600
                if str(d1.strftime('%A'))== "Friday":
                    segini=432000
                if str(d1.strftime('%A'))== "Saturday":
                    segini=518400
                if str(d1.strftime('%A'))== "Sunday":
                    segini=0

            h=float(hora[:2])*3600.0
            m=float(hora[2:-2])*60.0
            s=float(hora[-2:])
            doy_ant=doy

            sGPS.append(segini+(h+m+s))
        return sGPS
        
        
        
    def getLatitud(self):
        '''!
        @brief: Método que devuelve la latitud de cada observación,en formato pseudosexagesimal.
        @return [float]: Lista con la latitud convertida a formato pseudosexagesimal de cada observación.
        '''
        return [(float(i.split(",")[2][0:2])+(float(i.split(",")[2][2:4])/60.0)+(float(i.split(",")[2][4:])/60.0))
                if i.split(",")[3]=="N"
                else -(float(i.split(",")[2][0:2])+(float(i.split(",")[2][2:4])/60.0)+(float(i.split(",")[2][4:])/60.0))
                for i in self.__gga if i.split(",")[2]!=""]
    
    def getLongitud(self):
        '''!
        @brief: Método que devuelve la latitud de cada observación,en formato pseudosexagesimal.
        @return [float]: Lista con la longitud convertida a formato pseudosexagesimal de cada observación.
        '''
        return [(float(i.split(",")[4][0:3])+(float(i.split(",")[4][3:5])/60.0)+(float(i.split(",")[4][5:])/60.0))
                if i.split(",")[5]=="E"
                else -(float(i.split(",")[4][0:3])+(float(i.split(",")[4][3:5])/60.0)+(float(i.split(",")[4][5:])/60.0))
                for i in self.__gga if i.split(",")[4]!=""]
    
    def getAltitud(self):
        '''!
        @brief: Método que devuelve la altitud de cada observación.
        @return [float]: Lista con la altitud de cada observación.
        '''
        return [float(i.split(",")[9]) for i in self.__gga if i.split(",")[9]!=""]
    
    def getHDOP(self):
        '''!
        @brief: Método que devuelve el HDOP de cada observación.
        @return [float]: Lista con el HDOP de cada observación.
        '''
        return [float(i.split(",")[8]) for i in self.__gga if i.split(",")[8]!=""]
    
    def getNumeroSatelites(self):
        '''!
        @brief: Método que devuelve el HDOP de cada observación.
        @return [int]: Lista con el número de satélites de cada observación.
        '''
        return [int(i.split(",")[7]) for i in self.__gga if i.split(",")[7]!=""]
    
    def getMensajeGGA(self):
        '''!
        @brief: Método que devuelve el mensaje GGA completo.
        @return [str]: Lista con el mensaje GGA completo
        '''
        return self.__gga

    def getMensajeRMC(self):
        '''!
        @brief: Método que devuelve el mensaje RMC completo.
        @return [str]: Lista con el mensaje RMC completo.
        '''
        return self.__rmc
    
    def getOutListValues(self):
        '''!
        @brief: Devuelve los parámetros de cálculo mas importantes en una úncia lista.
        @return [segundos GPS,latitud,longitud,Altitud,número satélites, HDOP]
        '''
        sal=[]
        for seg,lat,lon,hel,sats,hdop in zip(self.getSegundosGPS(),self.getLatitud(),self.getLongitud(),
                                   self.getAltitud(),self.getNumeroSatelites(),self.getHDOP()):
            sal.append([seg,lat,lon,hel,sats,hdop])
        return sal
    
    def toSHP(self,Elipsoide,path=None):
        '''
        \brief Convierte el fichero NMEA a shp.
        param path str: Ruta en la que se quiere guardar el shp.
        '''
        #Por defecto la ruta sera la misma en la que se encuentre el fichero NMEA.
        import shapefile
        import Proyecciones.Geo2UTM as g2u
        import Geometrias.PuntoGeodesico as pgeo
        if path==None:
            path=self.__filepath
            
        if not exists(path):
            raise Exception("El fichero introducido no existe.")
        if not isfile(path):
            raise Exception("la ruta introducida no corresponde con un directorio.")
        
        w = shapefile.Writer(shapeType=8)
        w.field('X','F',10,4)
        w.field('Y','F',10,4)
        w.field('h','F',10,4)#Float
        #w.field('Fecha','D')#Date YYYYMMDD
        w.field('Hora','C',6)#String
        w.field('Segundos GPS','F',6,1)
        w.field('Huso','N',2)#int, número de valores.
        w.field('Satelites','N',3)
        w.field('HDOP','F',3,2)
        
        #print(len(self.getFechas()),len(self.getHoras()),len(self.getSegundosGPS()))
        
        
        for i,j,k,hora,sgps,sat,hdop in zip(self.getLatitud(),self.getLongitud(),self.getAltitud(),
                                  self.getHoras(),self.getSegundosGPS(),
                                  self.getNumeroSatelites(),self.getHDOP()):
            #print(sgps)
            sal=g2u.Geo2UTM(pgeo.PuntoGeodesico(i,j), Elipsoide)
            w.point(sal.getX(),sal.getY(),k,0)
            w.record(sal.getX(),sal.getY(),k,hora,sgps,sal.getHuso(),sat,hdop)
        w.save(self.__path+'/pruebaSHP')
        
        
            

        
    
        
        
    
def main():
    nmea=NMEAFile('../ejemplos/doy298_treal')
    nmea.toSHP('GRS 1980')
#     print(nmea.getDoys())
#     print(nmea.getFechas())
#     for i in nmea.getSegundosGPS():
#         print(i)
    #nmea.getLatitud()
    #nmea.getLongitud()
#     for i in nmea.getOutListValues():
#         print(i)

if __name__=="__main__":
    main()    
        
    
        
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 25/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo.
@version: 1.0.0
'''
import sys
sys.path.append('../..')


import Geometrias.PuntoGeodesico as pgeo
import BasesDeDatos.SQLite.SQLiteManager as DB


def CalcularOndulacion(PuntoGeodesico):
    '''
    Función para calcular la ondulación del Geoide del Modelo EGM08 del IGN.
    '''
    # Conexión a las bases de datos existentes.
    db1 = DB.SQLiteManager('EGM_Peninsula.db')
    db2 = DB.SQLiteManager('EGM_Canarias.db')
    # comprobar si el punto introducido puede ser calculado.
    lat = PuntoGeodesico.getLatitud()
    lon = PuntoGeodesico.getLongitud()
    
    vals1 = db1.ObtenerTodo('Cabecera')
    #print(vals1)
    lat1=vals1[0][0]
    lon1=vals1[0][1]
    ilat1=vals1[0][2]
    ilon1=vals1[0][3]
    fil1=vals1[0][4]
    col1=vals1[0][5]
    Alat=ilat1*fil1
    Alon=ilon1*col1
    lat1f=lat1-Alat
    lon1f=lon1+Alon
    if lon1f>=360:
        lon1f-=360
    #print(Alat,Alon,lat1f,lon1f)
    
    
    
    vals2 = db2.ObtenerTodo('Cabecera')
    #print(vals2)
    lat2=vals2[0][0]
    lon2=vals2[0][1]
    ilat2=vals2[0][2]
    ilon2=vals2[0][3]
    fil2=vals2[0][4]
    col2=vals2[0][5]
    Alat=ilat2*fil2
    Alon=ilon2*col2
    lat2f=lat2-Alat
    lon2f=lon2+Alon
    if lon2f>=360:
        lon2f-=360
    #print(Alat,Alon,lat2f,lon2f)
    
    
    
    lonaux=lon
    if lon<0:
        lonaux=lon+360
        
#     print(lonaux)
    
    incfil=0
    inccol=0
    onds1=None
    onds2=None
    lat_calc=0
    lon_calc=0
    
    if (lat<lat1 and lat>lat1f):
        if lonaux<360 and lonaux>lon1:
            print('Peninsula')
            diflat=lat1-lat
            diflon=lonaux-lon1
            incfil=int(diflat/ilat1)
            inccol=int(diflon/ilon1)
            onds1=db1.ObtenerFila('Ondulaciones', str(incfil))
            onds2=db1.ObtenerFila('Ondulaciones', str(incfil+1))
            lat_calc=lat1-ilat1*incfil
            lon_calc=lon1+ilon1*inccol
            if lon_calc>=360:
                lon_calc-=360
        elif lonaux>=0 and lonaux<lon1f:
            print('Peninsula')
            diflat=lat1-lat
            diflon=(360-lon1)+lonaux
            incfil=int(diflat/ilat1)
            inccol=int(diflon/ilon1)
            onds1=db1.ObtenerFila('Ondulaciones', str(incfil))
            onds2=db1.ObtenerFila('Ondulaciones', str(incfil+1))
            lat_calc=lat1-ilat1*incfil
            lon_calc=lon1+ilon1*inccol
            if lon_calc>=360:
                lon_calc-=360
    elif (lat<lat2 and lat>lat2f) and (lonaux>lon2 and lonaux<lon2f):
        print('Canarias')
        diflat=lat2-lat
        diflon=lonaux-lon2
        incfil=int(diflat/ilat2)
        inccol=int(diflon/ilon2)
        onds1=db2.ObtenerFila('Ondulaciones', str(incfil))
        onds2=db2.ObtenerFila('Ondulaciones', str(incfil+1))
        lat_calc=lat2-ilat2*incfil
        lon_calc=lon2+ilon2*inccol
        if lon_calc>=360:
            lon_calc-=360
    else:
        print('No valido')
        return None
    
#     print(onds1)
#     print(onds2)
    ond0=onds1[0][inccol+1]
    ond1=onds1[0][inccol]
    ond2=onds2[0][inccol+1]
    ond3=onds2[0][inccol]
    
#     print(ond0,ond1)
#     print(ond2,ond3)
#     print(lat_calc,lat)
#     print(lon_calc,lonaux)
    Alat=abs(lat_calc-lat)
    Alon=abs(lon_calc-lonaux)
#     print(Alat,Alon)
    
    #Interpolación bilineal.
    v1=ond0*Alon*Alat
    v2=ond1*(ilon1-Alon)*Alat
    v3=ond2*Alon*(ilat1-Alat)
    v4=ond3*(ilon1-Alon)*(ilat1-Alat)
    #print(v1,v2,v3,v4)
    return(v1+v2+v3+v4)/(ilat1*ilon1)





def main():
    p = pgeo.PuntoGeodesico(39.205324, -0.524532)  # Valor PAG: 50.256
    print(CalcularOndulacion(p))
    
    p = pgeo.PuntoGeodesico(39.205324, -0.495632)  # Valor PAG: 50.202
    print(CalcularOndulacion(p)) 
    
    p = pgeo.PuntoGeodesico(39.205324, 0.495632)  # Valor PAG: 48.127
    print(CalcularOndulacion(p))
    
    p = pgeo.PuntoGeodesico(40.505324, 0.495632)  # Valor PAG: 49.689
    print(CalcularOndulacion(p))
    
    p = pgeo.PuntoGeodesico(28.505324, 345.495632)  # Valor PAG:
    print(CalcularOndulacion(p))
    
    p = pgeo.PuntoGeodesico(58.505324, 345.495632)  # Valor PAG:
    print(CalcularOndulacion(p))
    
if __name__ == '__main__':
    main()
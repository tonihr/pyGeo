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
from datetime import datetime

class GPSNavigationReader(object):
    '''!
    classdocs
    '''


    def __init__(self, GPSNavigationFile):
        '''!
        Constructor
        '''
        #Comprobación del fichero.
        if not type(GPSNavigationFile)==str:
            raise Exception("La ruta del fichero introducido no es de tipo str.")
        if not exists(GPSNavigationFile):
            raise Exception("La ruta del fichero introducido no existe.")
        if not isfile(GPSNavigationFile):
            raise Exception("La ruta del fichero introducido no corresponde a ningun fichero.")
        
        if GPSNavigationFile.endswith("n") or GPSNavigationFile.endswith("N") and search("\d\d",GPSNavigationFile.split(".")[1]):
                pass
        else:
            raise Exception("La extensión del archivo no es válida.")

        self.head=[]
        self.body=[]
        
        f=open(GPSNavigationFile,'r')
        for i in f:
            if not "END OF HEADER" in i:
                self.head.append(i)
            else:
                break
        for i in f:
            self.body.append(i)
        f.close()
        
        
    def getHeader(self):
        '''!
        @brief: Función que devuelve los parametros informativos de la cabecera del fichero de nvegación GPS
        @return dict: Diccionario con los elementos de la cabecera.
        '''
        sal={}
        for i in self.head:
            if "LEAP SECONDS" in i[60:80]:
                sal.update({"LEAP SECONDS":float(" ".join(i[0:60].split()))})
                continue
            if "DELTA-UTC: A0,A1,T,W" in i[60:80]:
                sal.update({"A0":float(" ".join(i[0:22].split()).replace("D","E"))})
                sal.update({"A1":float(" ".join(i[22:41].split()).replace("D","E"))})
                sal.update({"T":int(" ".join(i[41:50].split()).replace("D","E"))})
                sal.update({"W":int(" ".join(i[50:60].split()).replace("D","E"))})
                continue
            #Añadir más cuando sea necesario.
        return sal
    
    def getNavigation(self):
        '''!
        @brief: Función que devulve el mensaje de navegacion.
        @return list: [época, satélite,[mensaje]]
        '''
        Sal=[]
        for indi,i in enumerate(self.body):
            if len(i.split())>=7:
                aux=self.body[indi:indi+8]
##                print(aux)
                val=[]
                date=None
                sat=None
                for indi1,j in enumerate(aux):
                    if indi1==0:
                        sat="".join(j[0:2].split())
                        if len(sat)==1:
                            sat="".join(('0',sat))
                            sat="".join(('G',sat))
                        elif len(sat)==2:
                            sat="".join(('G',sat)) 
                        date=datetime(2000+int(j[2:5]),int(j[5:8]),int(j[8:11]),int(j[11:14]),int(j[14:17]),int(j[17:22].split(".")[0]))
                        val.append(float(j[22:41].replace('D','E')))
                        val.append(float(j[41:60].replace('D','E')))
                        val.append(float(j[60:79].replace('D','E')))
                    else:
                        val.append(float(j[0:22].replace('D','E')))
                        try:
                            val.append(float(j[22:41].replace('D','E')))
                        except Exception as e:
                            val.append(None)
                        try:
                            val.append(float(j[41:60].replace('D','E')))
                        except Exception as e:
                            val.append(None)
                        try:
                            val.append(float(j[60:79].replace('D','E')))
                        except Exception as e:
                            val.append(None)
##                print(date)
##                print(sat)
##                input()
                insertar=[date,sat,val]
                if insertar in Sal:
                    continue
                else:
                    Sal.append([date,sat,val])
##        Sal=list(set(Sal))
        Sal.sort(key=lambda x: (x[1],x[0]))

        return Sal
        
        
        
def main():
    from os.path import  abspath,dirname,join
    from os import listdir
    rutasample=abspath(join(dirname( __file__ ),'..','ejemplos/unionRinex'))
##    print(rutasample)
    ficheros=listdir(rutasample)
    #print(ficheros)
    val=[i for i in ficheros if i.endswith("N")]
##    print(val)
    seleccionado=None
    for enum,i in enumerate(val):
        print("Presione "+str(enum)+" para mostrar "+i)
    seleccionado=input()
    rutadescom=rutasample+"/"+str(val[int(seleccionado)])

    nav=GPSNavigationReader(rutadescom)
    cab=nav.getHeader()
    try:
        print(cab["LEAP SECONDS"])
        print(cab["A0"])
        print(cab["A1"])
        print(cab["T"])
        print(cab["W"])
    except:
        pass
    bod=nav.getNavigation()
    for i in bod:
        print(i)
        input()





if __name__ == "__main__":
    main()
        
        
        
        
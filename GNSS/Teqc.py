#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 19/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from os import listdir,remove
from os.path import abspath,dirname,exists,join,isfile,split,realpath
from re import search
from platform import system
from subprocess import Popen,PIPE
from datetime import datetime

class Teqc(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor de la clase TEqc
        '''
        #Se comprueba si existe el directorio con las heramientas binarias.
        try:
            self.__rutabin=abspath(join(dirname( __file__ ), '..', 'bin'))
            if "Linux" in system():
                exists(self.__rutabin+'/Linux/teqc')
                self.__exe= self.__rutabin+'/Linux/teqc'
            elif "Windows" in system():
                exists(self.__rutabin+'/Windows/teqc')
                self.__exe= self.__rutabin+'/Windows/teqc'
        except Exception as e:
            raise Exception(e)
        
        
    def qualityCheck(self,RutaRINEXstandard,borrar=True):
        '''!
        @brief:
        @params RutaRINEXstandard str: Ruta del fichero rinex standard de extensión ".o"
        @params borrar bool: Borra los ficheros intermedios que genera teqc al realizar el quality check
        conservando el fichero de extensión *.yyS. En caso contrario no borrara ningún fichero.
        '''
        #Comprobación del fichero.########
        if not isinstance(RutaRINEXstandard, str):
            raise Exception("La ruta del fichero Rinex no es de tipo string.")

        if not isfile(RutaRINEXstandard):
            raise Exception("La ruta introducida no corresponde a ningun fichero.")
        
        path,file=split(realpath(RutaRINEXstandard))
        if (file.endswith("o") or file.endswith("O"))  and search("\d\d",file.split(".")[1]):
            pass
        else:
            raise Exception("El fichero introducido no es de tipo RINEX.")
        
        #Archivos en la carpeta donde se encuentra el fichero rinex standard antes de la ejecución
        archivos_path=listdir(path)
        try:
            p = Popen(self.__exe+' +qc '+'"'+RutaRINEXstandard+'"', shell=True, stdout=PIPE, stderr=PIPE)
            outs, errs =p.communicate()
            p.poll()
            #print(outs)
            #Comprobar los mensajes de error y en caso de excepción para la ejecución.
        except Exception as e:
            #print(e)
            if p.returncode==0:
                pass
            if p.returncode == 4294967295:
                #print(errs)
                return errs
            if p.returncode == -1:
                #print(errs)
                return errs
        
        archivos_path_depues=listdir(path)
        #Archivos que se pueden borrar después de la ejecuión si se indica en la opción, solo nombre.
        archivos_borrar=tuple(set(archivos_path_depues) & set(set(archivos_path_depues) ^ set(archivos_path)))
        archivos_path=None
        archivos_path_depues=None

        if borrar==True:
            for i in archivos_borrar:
                remove(path+"/"+i)
                print(i)
                
                
    def UnirRinex(self,FicherosUnir,intervalo,nombreSalida,ordenar=False):
        '''!
        @brief: Une varios fichero rinex en uno.
        @param FicherosUnir []: Ruta de todos los ficheros rinex a unir.
        @param intervalo int|str: Muestreo de épocas del nuevo fichero.
        @param nombresSalida str: Nombre del fichero resultante de la unión.
        '''
        
        if not isinstance(FicherosUnir, list):
            raise Exception("Se esperaba una lista como entrada en FicherosUnir.")
        
        if ordenar==True:
            FicherosUnir.sort()
            
        intervalo=str(intervalo)
        
        rutas=""
        for i in FicherosUnir:
            if not exists(i):
                raise Exception("El fichero: "+i+" no se encuentra en la ruta especificada.")
            if not isfile(i):
                raise Exception("La ruta: "+i+" no corresponde a ningun fichero.")
            rutas+=i+" "
        print(rutas)
            
        try:
            p = Popen(self.__exe+' -O.dec '
                                 +intervalo+' '+rutas+'>'+" "+nombreSalida
                                 , shell=True, stdout=PIPE, stderr=PIPE)
            outs, errs =p.communicate()
            p.poll()
            print(outs)
            #print(errs)
            #Comprobar los mensajes de error y en caso de excepción para la ejecución.
        except Exception as e:
            print(e)
            if p.returncode==0:
                pass
            if p.returncode == 4294967295:
                print(errs)
                return errs
            if p.returncode == -1:
                print(errs)
                return errs
            
    def CabeceraRinex(self,FicheroRinex):
        '''!
        @brief: Devuelve la información de la cabecera del fichero RINEX standard.

        @param FicheroRinex str: Ruta del fichero RINEX del que se quiere obtener la información.
        
        La función devuelve un diccionario con el contenido de la cabecera.
        @return: dict
        '''
        #Comprobación del fichero.########
        if type(FicheroRinex)!=str:
            raise Exception("La ruta del fichero Rinex no es de tipo string.")

        if not isfile(FicheroRinex):
            raise Exception("La ruta introducida no corresponde a ningun fichero.")
        
        path,file=split(realpath(FicheroRinex))
        if (file.endswith("o") or file.endswith("O"))  and search("\d\d",file.split(".")[1]):
            pass
        else:
            raise Exception("El fichero introducido no es de tipo RINEX.")
        
        p=None
        try:
            p = Popen(self.__exe+' +meta '+'"'+FicheroRinex+'"', shell=True, stdout=PIPE, stderr=PIPE)
            outs, errs =p.communicate()
            p.poll()
##            print(outs)
            #Comprobar los mensajes de error y en caso de excepción para la ejecución.
        except Exception as e:
            print(e)
            if p.returncode==0:
                pass
            if p.returncode == 4294967295:
                print(errs)
                return errs
            if p.returncode == -1:
                print(errs)
                return errs
        sal={}
        #Resultados obtenidos con Teqc.
        for i in outs.splitlines():
            i=i.decode().strip()
            if "filename:" in i:
                sal.update({"FILE":" ".join(i.split(":")[1].split())})
                continue
            if "file size (bytes):" in i:
                sal.update({"SIZE":" ".join(i.split(":")[1].split())})
                continue
            if "start date & time:" in i:
                date=" ".join(i[27:].split())
                date=date.split()
                fecha=date[0]
                hora=date[1]
                fecha=fecha.split("-")
                hora=hora.split(":")
                date=None
                date=datetime(int(fecha[0]),int(fecha[1]),int(fecha[2]),int(hora[0]),int(hora[1]),int(hora[2].split(".")[0]))
                sal.update({"DATE INI":date})
                continue
            if "final date & time:" in i:
                date=" ".join(i[27:].split())
                date=date.split()
                fecha=date[0]
                hora=date[1]
                fecha=fecha.split("-")
                hora=hora.split(":")
                date=None
                date=datetime(int(fecha[0]),int(fecha[1]),int(fecha[2]),int(hora[0]),int(hora[1]),int(hora[2].split(".")[0]))
                sal.update({"DATE END":date})
                continue
            if "sample interval:" in i:
                sal.update({"INTERVAL":" ".join(i.split(":")[1].split())})
                continue
            if "station name:" in i:
                sal.update({"NAME":" ".join(i.split(":")[1].split())})
                continue
            if "antenna type:" in i:
                sal.update({"ANTENNA":" ".join(i.split(":")[1].split())})
                continue
            if "station ID number:" in i:
                sal.update({"STATION ID":" ".join(i.split(":")[1].split())})
                continue
            if "antenna type:" in i:
                sal.update({"STATION ID":" ".join(i.split(":")[1].split())})
                continue
            if "antenna latitude (deg):" in i:
                sal.update({"LATITUDE":" ".join(i.split(":")[1].split())})
                continue
            if "antenna longitude (deg):" in i:
                sal.update({"LONGITUDE":" ".join(i.split(":")[1].split())})
                continue
            if "antenna elevation (m):" in i:
                sal.update({"ELEVATION":" ".join(i.split(":")[1].split())})
                continue
            if "RINEX version:" in i:
                sal.update({"RINEX VERSION":" ".join(i.split(":")[1].split())})
                continue
            #Añadir más resultados al diccionario.
        
        #Resultados obtenidos de la cabecera original.
        cab=[]
        with open(FicheroRinex,'r') as f:
            for i in f:
                if not "END OF HEADER" in i:
                    cab.append(i)
                else:
                    break
            f.close()
        for i in cab:
            if "APPROX POSITION XYZ" in i:
                i=i[0:60]
                sal.update({"X":" ".join(i[0:14].split())})
                sal.update({"Y":" ".join(i[14:28].split())})
                sal.update({"Z":" ".join(i[28:42].split())})
                continue
            if "ANTENNA: DELTA H/E/N" in i:
                i=i[0:60]
                sal.update({"DELTA H":" ".join(i[0:14].split())})
                sal.update({"DELTA E":" ".join(i[14:28].split())})
                sal.update({"DELTA N":" ".join(i[28:42].split())})
                continue
                 
        return sal
    
    def InformacionSatelites(self,FicheroRinex):
        '''!
        @brief: Devuleve el número de épocas de los satelites visibles para cada señal registrada.

        @param FicherosRinex str: Ruta del fichero RINEX del que se quiere obtener la información de los satélites.
        '''

        #Comprobación del fichero.########
        if type(FicheroRinex)!=str:
            raise Exception("La ruta del fichero Rinex no es de tipo string.")

        if not isfile(FicheroRinex):
            raise Exception("La ruta introducida no corresponde a ningun fichero.")
        
        path,file=split(realpath(FicheroRinex))
        if (file.endswith("o") or file.endswith("O"))  and search("\d\d",file.split(".")[1]):
            pass
        else:
            raise Exception("El fichero introducido no es de tipo RINEX.")

        p=None
        try:
            p = Popen(self.__exe+' -O.sum . '+'"'+FicheroRinex+'"', shell=True, stdout=PIPE, stderr=PIPE)
            outs, errs =p.communicate()
            p.poll()
##            print(outs)
            #Comprobar los mensajes de error y en caso de excepción para la ejecución.
        except Exception as e:
            print(e)
            if p.returncode==0:
                pass
            if p.returncode == 4294967295:
                print(errs)
                return errs
            if p.returncode == -1:
                print(errs)
                return errs
        return outs
    
    def getObservables(self,FicheroRinex,listaObs):
        '''
        @brief: Método que devuleve los observables registrados para cada señal

        @param FicherosRinex str: Ruta del fichero RINEX del que se quiere obtener la información de los satélites.

        @return []: La función devuelve una lista con la siguiente estructura:
                [Fecha,satélite,observable1,observable2,...]
                El orden de los observables sera el mismo  que el que se introduzca en la entrada del método.
'''

        #Comprobación del fichero.########
        if type(FicheroRinex)!=str:
            raise Exception("La ruta del fichero Rinex no es de tipo string.")

        if not isfile(FicheroRinex):
            raise Exception("La ruta introducida no corresponde a ningun fichero.")
        
        path,file=split(realpath(FicheroRinex))
        if (file.endswith("o") or file.endswith("O"))  and search("\d\d",file.split(".")[1]):
            pass
        else:
            raise Exception("El fichero introducido no es de tipo RINEX standard.")
        SAL=[]
        p=None
        for i in listaObs:
            try:
                p = Popen(self.__exe+' -O.obs '+'+'+i+' "'+FicheroRinex+'"', shell=True, stdout=PIPE, stderr=PIPE)
                outs, errs =p.communicate()
                p.poll()
            except Exception as e:
                print(e)
                if p.returncode==0:
                    pass
                if p.returncode == 4294967295:
                    print(errs)
                    return errs
                if p.returncode == -1:
                    print(errs)
                    return errs
            outs=outs.splitlines()
            Leer=False
            parcial=[]
            Sate=[]
            epo=[]
            cont2=0
            for indi,j in enumerate(outs):
                j=j.decode()
##                print(j)
##                input()
                if "COMMENT" == j[60:]:
                        continue
                if Leer:
                    if "".join(j[0:26].split())=="":
##                        print("no")
                        continue
                    j=j.split()
                    if len(j)>=8:
                        cont2=0
                        cont=0
                        Sate=[]
                        epo=[]
                        epo=datetime(2000+int(j[0]),int(j[1]),int(j[2]),int(j[3]),int(j[4]),int(j[5].split(".")[0]))
                        sats=j[7]
                        cont=0
                        #Se obtiene el valor del número de satélites.
                        for k in sats:
##                            print(k)
                            if "G"==k or "R"==k  or "E"==k :
                                break
                            else:
                                cont+=1
                        numsats=int(sats[:cont])
##                        print(numsats)
##                        print(cont)
                        #Se consigue en una linea todos los satelites disponibles.
                        allsats=None
                        if numsats>12:
                            restosats=outs[indi+1].decode()
                            allsats=sats[cont:]+"".join(restosats.split())
##                            allsats=allsats[cont:] 
                        else:
                            allsats=sats[cont:]
##                        print(allsats)
##                        input()

                        Sate=[]
                        cont=0
                        for k in allsats:
                            if k=="G" or k=="R" or k=="E":
                                Sate.append(allsats[cont:cont+3])
                                cont+=3
##                        print(Sate)
##                        input()
                    else: 
                        parcial.append([epo,Sate[cont2],j])
                        cont2+=1
##                        print(cont2)
                if "END OF HEADER" == str(j[60:73]):
##                    print(j)
                    Leer =True
                    continue
##                for t in parcial:
##                    print(t)
##                input()

        return parcial

##            SAL.append(parcial)
##            parcial=[]
##
##        Final=[]
##        val=len(SAL)
##
##        for indi,j in enumerate(SAL[0]):
##            aux=[j[0],j[1]]
##            for t in range(val):
##                aux.append(SAL[t][indi][2])
##            Final.append(aux)
##        SAL=None
##        return Final

        
        
        
        
def main():
    rutasample=abspath(join(dirname( __file__ ),'..','ejemplos'))
    print(rutasample)
    ficheros=listdir(rutasample)
    print(ficheros)
    val=[i for i in ficheros if i.endswith("o")]
    print(val)
    seleccionado=None
    for enum,i in enumerate(val):
        print("Presione "+str(enum)+" para mostrar "+i)
    seleccionado=input()
    rutadescom=rutasample+"/"+str(val[int(seleccionado)])
    print(rutadescom)   
    rin=Teqc()
    print("----------------------------------------------")
    rin.qualityCheck(rutadescom,borrar=True)
    #Union de ficheros Rinex.
#     rutaunion=rutasample+"/unionRinex"
#     validos=[]
#     for i in listdir(rutaunion):
#         if 'VALE' in i and (i.endswith('o') or i.endswith('O')):
#             validos.append(rutaunion+"/"+i)
#     rin.UnirRinex(validos, 10, 'VALE_UNION_10',ordenar=True)
    print("----------------------------------------------")
    js=rin.CabeceraRinex(rutadescom)
    print(js)
#     from json import dumps
#     print(dumps(js, ensure_ascii=False)) # Para convertir el dict a json
    print("----------------------------------------------")
    print(rin.InformacionSatelites(rutadescom))
    
    print("----------------------------------------------")
    print(rin.getObservables(rutadescom, ['L1','C1']))


if __name__ == "__main__":
    main()
        
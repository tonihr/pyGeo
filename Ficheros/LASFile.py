#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 9/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
#TO-DO:
#Añadir opciones de autoborrado.
#Añadir opcion para comprobar si el fichero txt ya existe.


class LASFile(object):
    '''!
    classdocs
    '''
    __Xu=False#-X X sin escala.
    __Yu=False#-Y Y sin escala.
    __Zu=False#-Z Z sin escala.
    __a=False#-a angulo de escaneo.
    __n=False#-n Número de retornos por eco
    __r=False#-r Número del retorno.
    __c=False#-c Número de clasificacion.
    __Cu=False#-C Nombre de clasificación.
    __u=False#-u - user data
    __p=False#-p - point source ID
    __e=False#-e - edge of flight line
    __d=False#-d - direction of scan flag
    __rutaLAS=None
    __rutaTXT=None
    __intensidad=True#-i
    __rojo=True#-R
    __verde=True#-G
    __azul=True#-B
    
    __NombresColumnas=False
    __EnFichero=True
    __parse=''
    


    def __init__(self, FicheroLAS):
        '''!
        Constructor de la clase LASFile
        '''
        self.__CheckFichero(FicheroLAS)
        
        
    def __CheckFichero(self,FicheroLAS):
        '''!
        '''
        from os.path import exists,isfile,split
        if not exists(FicheroLAS):
            raise Exception("El fichero introducido no existe.")
        if not isfile(FicheroLAS):
            raise Exception("La ruta introducida no coincide con un fichero")
        ruta,fichero=split(FicheroLAS)
        if not fichero.lower().endswith("las"):
            raise Exception("Se esperaba un fichero de extension las")
        self.__rutaLAS=FicheroLAS
        
        
    def setRutaTxt(self,rutaTXT=None):
        '''!
        '''
        #Comprobar si ya se ha introducido alguna ruta. y la nueva ruta no es la misma.
        if rutaTXT!=None and self.__rutaTXT==rutaTXT:
            return
        if rutaTXT==None:
            from os.path import split
            path,filename=split(self.__rutaLAS)
            self.__rutaTXT=path+'/'+filename.split('.')[0]+'.txt'
        else:
            f=open(rutaTXT,'w')
            f.close()
            self.__rutaTXT=rutaTXT
        
    def incluirAnguloEscaneo(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__a=Incluir
        
    def incluirIntensidad(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__intensidad=Incluir
        
    def incluirRojo(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__rojo=Incluir
        
    def incluirVerde(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__verde=Incluir
        
    def incluirAzul(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__azul=Incluir
        
    def incluirRawX(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__Xu=Incluir
        
    def incluirRawY(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__Yu=Incluir
        
    def incluirRawZ(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__Zu=Incluir
        
    def incluirNombresColumnas(self,Incluir):
        '''!
        '''
        try:
            Incluir=bool(Incluir)
        except Exception as e:
            raise Exception(e)
        self.__NombresColumnas=Incluir
    
    def salidaEnFichero(self,EnFichero):
        '''!
        '''
        try:
            EnFichero=bool(EnFichero)
        except Exception as e:
            raise Exception(e)
        self.__EnFichero=EnFichero
        
    def parser(self):
        '''!
        '''
        comando=''
        self.__parse="xyz"
        if self.__intensidad==True:
            self.__parse+="i"
        if self.__Xu==True:
            self.__parse+='X'
        if self.__Yu==True:
            self.__parse+='Y'
        if self.__Zu==True:
            self.__parse+='Z'
        if self.__rojo==True:
            self.__parse+="R"
        if self.__verde==True:
            self.__parse+="G"
        if self.__azul==True:
            self.__parse+="B"
        if self.__a==True:
            self.__parse+="a"
            
        comando+='las2txt -i '+'"'+self.__rutaLAS+'"'
        if self.__EnFichero:
            self.setRutaTxt()
            comando+=' -o'+'"'+self.__rutaTXT+'"'
        comando+=' --parse '+self.__parse
        
        if self.__NombresColumnas==True:
            comando+=' --labels'
        if not self.__EnFichero:
            comando+=' --stdout'
        print(comando)
        return comando
        
        
    def Convertir(self):
            
        from subprocess import Popen,PIPE
        try:
            p1=Popen(self.parser(), shell=True, stdout=PIPE, stderr=PIPE)
            outs, errs =p1.communicate()
            p1.poll()
            return outs
        except Exception as e:
            if p1.returncode==0:
                return outs
            if p1.returncode == 1:
                return errs
            if p1.returncode == 2:
                return errs
            
    def toSHP(self,RutaSHP=None):
        '''!
        \brief Convierte el archivo LAS a shp.
        \para RutaSHP str: Ruta donde se guardara el SHP. si no se introduce, se creara con el mismo nombre que el fichero LAS.
        '''
        import shapefile
        if RutaSHP==None:
            from os.path import split
            path,filename=split(self.__rutaLAS)
            RutaSHP=path+'/'+filename.split('.')[0]
        self.salidaEnFichero(False)
        self.incluirNombresColumnas(True)
        sal=self.Convertir()
        sal=sal.decode().split('\n')
        w = shapefile.Writer(shapeType=8)
        #Leer cabecera del fichero TXT y crear los campos del fichero SHP.
        cab=sal[0]
        cab=cab.replace('"','')
        cab=cab.split(',')
        #print(cab)
        if 'X' in cab:
            w.field('X','F',10,4)
        if 'Y' in cab:
            w.field('Y','F',10,4)
        if 'Z' in cab:
            w.field('Z','F',10,4)
        if 'Intensity' in cab:
            w.field('Intensity','C',6)
        if 'Raw X' in cab:
            w.field('Raw X','C',7)
        if 'Raw Y' in cab:
            w.field('Raw Y','C',7)
        if 'Raw Z' in cab:
            w.field('Raw Z','C',7)
        if 'Red' in cab:
            w.field('Red','C',3)
        if 'Green' in cab:
            w.field('Green','C',3)
        if 'Blue' in cab:
            w.field('Blue','C',3)
        if 'Scan Angle' in cab:
            w.field('Scan Angle','C',3)
        if 'Number of Returns' in cab:
            w.field('Number of Returns','C',3)
        if 'Return Number' in cab:
            w.field('Return Number','C',3)
        if 'Classification' in cab:
            w.field('Classification','C',3)
        if 'Classification Name' in cab:
            w.field('Classification Name','T',30)
        if 'User Data' in cab:
            w.field('User Data','T',30)
        if 'Point Source ID' in cab:
            w.field('Point Source ID','C',9)
        if 'Flight Line Edge' in cab:
            w.field('Flight Line Edge','C',3)
        if 'Scan Direction' in cab:
            w.field('Scan Direction','C',3)
        if 'ID' in cab:
            w.field('ID','C',9)
        #print(w.fields)
        for i in sal[1:-1]:
            i=i.split(',')
            w.point(float(i[0]),float(i[1]),float(i[2]),0)
            w.records.append(i)
        w.save(RutaSHP)
        #Volver a poner las opciones del parse tal y como estaban.
    
    def getIncluirRojo(self):
        '''!
        '''
        return self.__rojo
        
        
        
        
        
def main():
    las=LASFile('../ejemplos/LIDAR.las')
    #print(las.Convertir())
    las.toSHP(RutaSHP=None)
    pass


if __name__=="__main__":
    main()    
        
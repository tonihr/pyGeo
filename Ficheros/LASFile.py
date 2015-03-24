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


class LASFile(object):
    '''!
    classdocs
    '''
    __rutaLAS=None
    __rutaTXT=None
    __intensidad=True
    __rojo=True
    __verde=True
    __azul=True


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
        
        
    def setRutaTxt(self,rutaTXT):
        '''!
        '''
        f=open(rutaTXT,'w')
        f.close()
        self.__rutaTXT=rutaTXT
        
    def incluirIntensidad(self,Incluir):
        '''!
        '''
        self.__intensidad=Incluir
        
    def incluirRojo(self,Incluir):
        '''!
        '''
        self.__rojo=Incluir
        
    def incluirVerde(self,Incluir):
        '''!
        '''
        self.__verde=Incluir
        
    
    def incluirAzul(self,Incluir):
        '''!
        '''
        self.__azul=Incluir
        
        
    def Convertir(self):
        if self.__rutaTXT==None:
            from os.path import split
            path,filename=split(self.__rutaLAS)
            self.__rutaTXT=path+'/'+filename.split('.')[0]+'.txt'
            
        from subprocess import Popen,PIPE
        
        parse="xyz"
        if self.__intensidad==True:
            parse+="i"
        if self.__rojo==True:
            parse+="R"
        if self.__verde==True:
            parse+="G"
        if self.__azul==True:
            parse+="B"
            
        try:
            p1=Popen('las2txt'+
                     ' -i '+
                     '"'+self.__rutaLAS+'"'+
                     ' -o'+
                     '"'+self.__rutaTXT+'"'
                     ' --parse '+parse, shell=True, stdout=PIPE, stderr=PIPE)
            outs, errs =p1.communicate()
            p1.poll()
            return 
        except Exception as e:
            if p1.returncode==0:
                return outs
            if p1.returncode == 1:
                return errs
            if p1.returncode == 2:
                return errs
        
        
        
def main():
    las=LASFile('../ejemplos/LIDAR.las')
    #las.Convertir()
    pass


if __name__=="__main__":
    main()    
        
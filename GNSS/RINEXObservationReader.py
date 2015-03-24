#!/usr/bin/env python
# -*- coding: utf-8 -
'''
Created on 2/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

import GNSS.Teqc as t

class RINEXObservationReader(object):
    '''
    classdocs
    '''


    def __init__(self, RINEXFile):
        '''
        Constructor
        
        @param RinexFile str: Ruta donde se encuentra el archivo RINEX standard.
        '''
        self.teqc=t.Teqc()
        self.f=RINEXFile
    def getHeader(self):
        return self.teqc.CabeceraRinex(self.f)
    def getObservation(self,obs):
        return self.teqc.getObservables(self.f,obs)
    
    
    
def main():
    from os.path import abspath,dirname,join
    from os import listdir
    rutasample=abspath(join(dirname( __file__ ),'..','ejemplos/unionRinex'))
##    print(rutasample)
    ficheros=listdir(rutasample)
    print(ficheros)
    val=[i for i in ficheros if i.endswith("o")]
##    print(val)
    seleccionado=None
    for enum,i in enumerate(val):
        print("Presione "+str(enum)+" para mostrar "+i)
    seleccionado=input()
    rutadescom=rutasample+"/"+str(val[int(seleccionado)])

    rin=RINEXObservationReader(rutadescom)
    print(rin.getHeader())
    obs=rin.getObservation(["C1","P2"])
    for i in obs:
        print(i)

if __name__ == "__main__":
    main()
        
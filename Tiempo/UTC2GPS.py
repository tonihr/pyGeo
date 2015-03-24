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


def UTC2GPS(fecha):
    '''
    @brief: Método para convertir un objeto de la clase datetime a tiempo GPS
    @param fecha datetime: Objeto de la clase datetine con la fecha a transformar en tiempo GPS.
    '''
    #doy=fecha.strftime('%j')
    name=fecha.strftime('%A')

    if name=="Sunday" or name=="Domingo":
        return 0+int(fecha.strftime('%H'))*3600+int(fecha.strftime('%M'))*60+int(fecha.strftime('%S'))
    if name=="Monday" or name=="Lunes":
        return 86400+int(fecha.strftime('%H'))*3600+int(fecha.strftime('%M'))*60+int(fecha.strftime('%S'))
    if name=="Tuesday" or name=="Martes":
        return 172800+int(fecha.strftime('%H'))*3600+int(fecha.strftime('%M'))*60+int(fecha.strftime('%S'))
    if name=="Wednesday" or name=="Miércoles":
        return 259200+int(fecha.strftime('%H'))*3600+int(fecha.strftime('%M'))*60+int(fecha.strftime('%S'))
    if name=="Thursday" or name=="Jueves":
        return 345600+int(fecha.strftime('%H'))*3600+int(fecha.strftime('%M'))*60+int(fecha.strftime('%S'))
    if name=="Friday" or name=="Viernes":
        return 432000+int(fecha.strftime('%H'))*3600+int(fecha.strftime('%M'))*60+int(fecha.strftime('%S'))
    if name=="Saturday" or name=="Sábado":
        return 518400+int(fecha.strftime('%H'))*3600+int(fecha.strftime('%M'))*60+int(fecha.strftime('%S'))


def main():
    from datetime import datetime
    print(UTC2GPS(datetime(2014,10,28,17,0,0)))
    

if __name__=="__main__":
    main()
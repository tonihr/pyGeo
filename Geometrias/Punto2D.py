#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 29/1/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

class Punto2D(object):
    '''!
    Clase destinada al almacenamiento de la información espacial de un punto bidimensional.
    Ejemplos de declaración del un objeto de la clase:\n
    p=Punto2D()-->Constructor vacío.\n
    p=Punto2D(10,10)\n
    p=Punto2D(10,10,negativos=True)\n
    p=Punto2D(10,10,negativos=False)\n
    p=Punto2D(-10,-10,negativos=False)-->Error.\n
    '''
    __X = None
    __Y = None
    __neg = True

    def __init__(self, *args, **kwargs):
        '''
        Constructor de la clase Punto2D.
        
        Args:
            param1 (float): Valor de la coordenada X.
                                    X coordinate value.
            param2 (float):Valor de la coordenada Y.
                                    Y coordinate value.
                
        Kwargs:
            negativos (bool): Estado de la propiedad negativos.
                                    Negative property status.
            
        Raises:
            ArgumentError: Se producira una excepción si se introducen más o menos argumentos de los admitidos por la clase.
            KeyWordError: Se producira una excepción si no se reconoce el kwarg introducido.
        '''
        # Parsear los kwargs.
        if len(kwargs) > 0:
            for key in kwargs:
                if key.lower() == 'negativos':
                    aux = kwargs[key]
                    self.setNegativos(aux)
                else:
                    raise Exception("El argumento: " + key + " no se reconoce")
            
        # Parsear args.
        if len(args) == 0:
            pass
        elif len(args) == 2:
            self.setX(args[0])
            self.setY(args[1])
        else:
            raise Exception("La clase Punto2D recibe 2 parametros como argumentos.\nSe han introducido: " + str(len(args)) + " parametros.")
            
        
    def setX(self, X):
        '''!
        @brief: Método para introducir el valor de la coordenada X de un punto.
        @param X float: Valor de la coordenada.
        @exception: Se producira una excepción si el valor introducido no se puede convertir a un número.
        @exception: Se producira una excepción si se introduce un valor negativo con la propiedad negativos=False.
        '''
        if isinstance(X, str) or isinstance(X, int) or isinstance(X, float):
            # Se comprueba el tipo de dato introducido y se intenta convertir a float.
            try:
                self.__X = float(X)
            except Exception as e:
                raise Exception(e)
        else:
            raise ValueError()
        
        if self.__neg == False and self.__X < 0:
            # En el caso de que el valor sea negativo y no se puedan introducir números negativos saltara la excepción.
            raise Exception("La coordenada X no puede ser negativa.\nNegativos=" + str(self.__neg))
        
        
    def setY(self, Y):
        '''!
        @brief: Método para introducir el valor de la coordenada Y de un punto.
        @param Y float: Valor de la coordenada.
        @exception: Se producira una excepción si el valor introducido no se puede convertir a un número.
        @exception: Se producira una excepción si se introduce un valor negativo con la propiedad negativos=False.
        '''
        if isinstance(Y, str) or isinstance(Y, int) or isinstance(Y, float):
            # Se comprueba el tipo de dato introducido y se intenta convertir a float.
            try:
                self.__Y = float(Y)
            except Exception as e:
                raise Exception(e)
        else:
            raise ValueError()
        
        if self.__neg == False and self.__Y < 0:
            # En el caso de que el valor sea negativo y no se puedan introducir números negativos saltara la excepción.
            raise Exception("La coordenada Y no puede ser negativa.\nNegativos=" + str(self.__neg))
    
    def setFromWKT(self, wkt):
        '''!
        @brief: Añade un punto a partir de un string en formato wkt.
        @param wkt str: Un string en formato wkt.
        '''
        coor = wkt.split('POINT')[1]
        coor = coor.replace('(', '')
        coor = coor.replace(')', '')
        coor = coor.split()
        self.setX(coor[0])
        self.setY(coor[1])
        
    def setFromGeoJSON(self, geojson):
        '''!
        @brief: Añade un punto a partir de un string en formato geojson.
        @param geojson str: Un string en formato geojson.
        '''
        from json import loads
        coors = loads(geojson)
        if coors['type'] != 'Point':
            raise Exception("El GeoJSON introducido no corresponde con un punto")
        else:
            coor = coors['coordinates']
            self.setX(coor[0])
            self.setY(coor[1])
            
    def setNegativos(self, Negativos):
        '''!
        @brief: Método para introducir la propiedad Negativos.
        @param Neagativos bool|str|int: Estado de la propiedad Negativos.
        @note Neagativos True: Permite alojar números negativos.
        @note Neagativos False: No permite alojar números negativos.
        @exception: Se producira una excepción si el valor introducido no se puede convertir a bool.
        @exception: Se producira una excepcion si se cambia la propiedad negativos a Flase y existen coordenadas negativas en la clase.
        '''
        if isinstance(Negativos, bool) or isinstance(Negativos, str) or isinstance(Negativos, int):
            # Se comprueba el tipo de dato introducido y se intenta convertir a bool.
            try:
                self.__neg = bool(Negativos)
            except Exception as e:
                raise Exception(e)
            
        if self.__neg == False:
            # En el caso de que no se puedan introducir números negativos y la clase contenga algún valor
            # en las coordenadas X e Y, si estas son negativas saltara una excepción.
            if self.__X != None and self.__X < 0:
                raise Exception("La coordenada X de la clase es negativa.")
            if self.__Y != None and self.__Y < 0:
                raise Exception("La coordenada Y de la clase es negativa.")
            
            
    def getX(self):
        '''!
        @brief: Método que devuelve el valor de la coordenada X almacenada.
        @return float: Valor de la coordenada X.
        '''
        return self.__X
    
    def getY(self):
        '''!
        @brief: Método que devuelve el valor de la coordenada Y almacenada.
        @return float: Valor de la coordenada Y.
        '''
        return self.__Y
    
    def getNegativos(self):
        '''!
        @brief: Método que devuelve el valor actual de la propiedad negativos.
        @return bool: Estado de la propiedad Negativos.
        '''
        return self.__neg
    
    def toString(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato str.
        @return str: Un string con toda la información del punto.
        '''
        return "X:" + str(self.__X) + "\n"\
            "Y:" + str(self.__Y) + "\n"\
            "Negativos:" + str(self.__neg) + "\n"
            
    def toJSON(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato JSON.
        @return str: Un string en formato JSON.
        '''
        return "{\n" + \
            '"X":' + '"' + str(self.__X) + '"' + ",\n"\
            '"Y":' + '"' + str(self.__Y) + '"' + ",\n"\
            '"Negativos":' + '"' + str(self.__neg) + '"' + "\n"\
            + "}"
            
    def toGeoJSON(self):
        '''!
        @brief: Método que devuleve un GeoJSON del punto.
        @return str: Un string en formato JSON.
        '''
        
        return "{\n" + \
            '"type":"Point"' + ",\n"\
            '"coordinates":' + \
            '[' + str(self.__X) + ',' + str(self.__Y) + ']' + "\n"\
            "}"
            
    def toWKT(self):
        '''!
        @brief: Método que devuleve un wkt del punto.
        @return str: Un string en formato wkt.
        '''
        return 'POINT (' + str(self.__X) + ' ' + str(self.__Y) + ')'
                
def main():
    from json import loads
    p1 = Punto2D(-10, 20, NEGATIVOS=True)
#     print(p1.toString())
#     print(p1.toJSON())
#     print(json.loads(p1.toJSON())['X'])
    print(p1.toGeoJSON())
    print(loads(p1.toGeoJSON())['coordinates'])
    print(p1.toWKT())
    
    p1.setFromWKT('POINT (50 50)')
    print(p1.toWKT())
    
    geojson = '{"type":"Point","coordinates":[-10.0,20.0]}'
    p1.setFromGeoJSON(geojson)
    print(p1.toWKT())
#     p1.setNegativos(False)
    
if __name__ == "__main__":
    main()
        

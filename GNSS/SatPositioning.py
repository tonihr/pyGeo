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
import Tiempo.UTC2GPS as u2g
from math import sqrt,cos,sin,atan2,floor
from numpy import matrix,dot,array
import Geometrias.Angulo as ang

class SatPositioning(object):
    '''
    classdocs
    '''



    def __init__(self, Efems,Obs):
        '''
        Constructor 
        '''
        self.ef=Efems
        self.obs=Obs
        
    def getPosition(self):
        #Cte más adelante cambiar por los valores de los elipsoides en la base de datos.
        c=2.99792458e8
        GM=3.986005e14
        we=7.2921151467e-5
        F=-4.442807633e-10
        
        #Cálculo de la posicion para cada satelite en funcion de la epoca.
        Sal=[] #se almacenan los valores de salida.
        
        for j in self.obs: #Para cada tipo de observable con el que se quiera calcular.
            tipo=j[1] #Tipo de observable:
            if "G" in tipo: #Observable GPS:
                #Calcular la efemeride más cercana para el observable.
                Dif=[]
                for indi,i in enumerate(self.ef):
                    if i[1]==j[1]:
                        t_obs=u2g.UTC2GPS(j[0])
                        t_efem=u2g.UTC2GPS(i[0])
                        Dif.append([t_efem-t_obs,indi])
                if Dif==[]:
                    continue
                vali=Dif[0]
                for i in Dif:
                    if i[0]<vali[0]:
                        vali=i
                        
                #Efemeride GPS.
                t=u2g.UTC2GPS(j[0])     #Tiempo de la observación.
                #se debe corregir del tiempo de viaje de la señal asi como de efectos atmosfericos si los datos estan disponibles.
                t=t-(float(j[2][0]))/c  #Tiempo corregido de los efectos.
                
                vali=self.ef[vali[1]]
                #Valores de la efemerides. Comprobar si la posición cambia entre diferentes versiones de ficheros RINEX
                af0=vali[2][0]
                af1=vali[2][1]
                af2=vali[2][2]
                Crs=vali[2][4]
                delta_n=vali[2][5]
                M0=vali[2][6]
                Cuc=vali[2][7]
                ecc=vali[2][8]
                Cus=vali[2][9]
                a=vali[2][10]**2
                toe=vali[2][11]
                Cic=vali[2][12]
                OMEGA=vali[2][13]
                Cis=vali[2][14]
                I0=vali[2][15]
                Crc=vali[2][16]
                Omega=vali[2][17]
                OMEGA_DOT=vali[2][18]
                IDOT=vali[2][19]
                week=vali[2][20]
                tgd=vali[2][24]
                time_trans=vali[2][26]
                
                tk=t-toe
                Atsv=af0+af1*(tk)+af2*(tk)**2
                tk=tk-Atsv-tgd
                M=M0+((sqrt((GM)/(a**3)))+(delta_n))*tk
                M=ang.Angulo(M,girar=True)
                M=M.getAngulo()
                E_ant=M
                E_sig=0
                while(abs(E_ant-E_sig)!=0):
                    E_sig=M+ecc*sin(E_ant)
                    E_ant=E_sig
                E=ang.Angulo(E_sig)
                E=E.getAngulo()
                tk=tk+(F*ecc*sqrt(a)*sin(E))
                true_anom=atan2((sqrt(1-ecc**2)*sin(E)),(cos(E)-ecc))
                alfa=ang.Angulo(2*(true_anom+Omega),girar=True)
                alfa=alfa.getAngulo()
                Omega1=ang.Angulo(Omega+(Cuc*cos(alfa))+(Cus*sin(alfa)),girar=True)
                Omega1=Omega1.getAngulo()
                incli=ang.Angulo((I0+(IDOT*tk))+(Cic*cos(alfa))+(Cis*sin(alfa)),girar=True)
                incli=incli.getAngulo()
                r=(a*(1-(ecc*cos(E))))+(Crc*cos(alfa))+(Crs*sin(alfa))
                OMEGA_FIN=ang.Angulo(OMEGA+((OMEGA_DOT-we)*tk)-(we*toe),girar=True)
                OMEGA_FIN=OMEGA_FIN.getAngulo()

                K=matrix([[r*cos(true_anom)],
                            [r*sin(true_anom)],
                            [0]])
                
                R=matrix([[cos(OMEGA_FIN)*cos(Omega1)-sin(OMEGA_FIN)*sin(Omega1)*cos(incli),-cos(OMEGA_FIN)*sin(Omega1)-sin(OMEGA_FIN)*cos(Omega1)*cos(incli),sin(OMEGA_FIN)*sin(incli)],
                            [sin(OMEGA_FIN)*cos(Omega1)+cos(OMEGA_FIN)*sin(Omega1)*cos(incli),-sin(OMEGA_FIN)*sin(Omega1)+cos(OMEGA_FIN)*cos(Omega1)*cos(incli),-cos(OMEGA_FIN)*sin(incli)],
                            [sin(Omega1)*sin(incli),cos(Omega1)*sin(incli),cos(incli)]])
                sol=dot(R,K)
                X=float(sol[0])
                Y=float(sol[1])
                Z=float(sol[2])
    ##            print(X,Y,Z)
    ##            print(i[1],E_sig,true_anom,alfa,Omega1,incli,r,OMEGA_FIN,float(j[2][0]))
                Sal.append([j[0],j[1],X,Y,Z,float(j[2][0]),Atsv])
                
            elif "R" in tipo:
                #Calcular la efemeride más cercana para el observable.
                Dif=[]
                for indi,i in enumerate(self.ef):
                    if i[1]==j[1]:
                        t_obs=u2g.UTC2GPS(j[0])
                        t_efem=u2g.UTC2GPS(i[0])
                        Dif.append([t_efem-t_obs,indi])
                if Dif==[]:
                    continue
                vali=Dif[0]
                for i in Dif:
                    if i[0]<vali[0]:
                        vali=i
                vali=self.ef[vali[1]]
                #Efemeride GLONASS.
                tefem=vali[0]
                tobs=j[0]
                tau=vali[2][0]
                gamma=vali[2][1]
                tk=vali[2][2]
                X=vali[2][3]*1000
                vx=vali[2][4]*1000
                ax=vali[2][5]*1000
                health=vali[2][6]
                Y=vali[2][7]*1000
                vy=vali[2][8]*1000
                ay=vali[2][9]*1000
                f=vali[2][10]
                Z=vali[2][11]*1000
                vz=vali[2][12]*1000
                az=vali[2][13]*1000
                age=vali[2][14]
                #Corregir tiempo.
                t=(u2g.UTC2GPS(tobs)-u2g.UTC2GPS(tefem))
                t=t-(float(j[2][0]))/c
                #Error del reloj del satélite.
                Atsv=-tau+gamma*t
                t=t-Atsv
                 
                #Calcular la posicion correcto.
                ##Interpolacion de la posicion por el metodo de Ringe-Kutta 4º orden.
##                print(X,Y,Z)
#                 Xsal=X+vx*t+ax*t**2
#                 Ysal=Y+vy*t+ay*t**2
#                 Zsal=Z+vz*t+az*t**2

#                 print(Xsal,Ysal,Zsal)
                pasos=30
                itera=floor(abs(t/pasos))
##                print(itera)
##
                Xa=X
                Ya=Y
                Za=Z
                vxa=vx
                vya=vy
                vza=vz

#                 for s in range(itera):
#                     err=t/itera
# #                     print(err)
#                     sal1=sat_pos.Sat_Motion_Dif(Xa,Ya,Za,vxa,vya,vza,ax,ay,az,Elip.Elipsoides('PZ-90'))
# #                     print(sal1)
#                     sal2=sat_pos.Sat_Motion_Dif(Xa+(sal1[0]*err/2),Ya+(sal1[1]*err/2),Za+(sal1[2]*err/2),vxa+(sal1[3]*err/2),vya+(sal1[4]*err/2),vza+(sal1[5]*err/2),ax,ay,az,Elip.Elipsoides('PZ-90'))
# #                     print(sal2)
#                     sal3=sat_pos.Sat_Motion_Dif(Xa+(sal2[0]*err/2),Ya+(sal2[1]*err/2),Za+(sal2[2]*err/2),vxa+(sal2[3]*err/2),vya+(sal2[4]*err/2),vza+(sal2[5]*err/2),ax,ay,az,Elip.Elipsoides('PZ-90'))
# #                     print(sal3)
#                     sal4=sat_pos.Sat_Motion_Dif(Xa+sal3[0]*err,Ya+sal3[1]*err,Za+sal3[2]*err,vxa+sal3[3]*err,vya+sal3[4]*err,vza+sal3[5]*err,ax,ay,az,Elip.Elipsoides('PZ-90'))
# #                     print(sal4)
#                     sal=array([Xa,Ya,Za,vxa,vya,vza])+(array(sal1)+2*array(sal2)+2*array(sal3)+array(sal4))*err/6
# #                     print(err)
# #                     print(sal)
# #                     input()
#                     Xa=sal[0]
#                     Ya=sal[1]
#                     Za=sal[2]
#                     vxa=sal[3]
#                     vya=sal[4]
#                     vza=sal[5]
#                 print(Xa,Ya,Za)
#                 input()
                 
                #Cambiar de marco.
                ##Parametros Boucher-Altamini.
                Tx=-0.36
                Ty=0.08
                Tz=0.018
#                 Tx=0.07
#                 Ty=0.0567
#                 Tz=-0.7733
#                 wx=-9.2114599410812E-11
#                 wy=-1.9392547244381E-11
#                 wz=1.7113922943167E-9
#                 d=-3/10E9
                ##Transformacion de 7 parametros de Helmert.
                Xsal=Xa+Tx
                Ysal=Ya+Ty
                Zsal=Za+Tz

                Sal.append([j[0],j[1],Xsal,Ysal,Zsal,float(j[2][0]),Atsv])   
        return Sal
    
    
    
    
    
def main():
    #Leer un fichero de navegación.
    import GNSS.GPSNavigationReader as nav_r
    import GNSS.GLONASSNavigationReader as nav_g
    import GNSS.RINEXObservationReader as rin_obs
    nav1=nav_r.GPSNavigationReader('/home/toni/Dropbox/LibGeo/Ejemplos/VCIA2710.14n')
    #nav2=nav_g.GLONASS_Nav_Reader('/home/toni/Dropbox/LibGeo/Ejemplos/VCIA2710.14g')
    rin=rin_obs.RINEXObservationReader('/home/toni/Dropbox/LibGeo/Ejemplos/VCIA2710.14o')
    Efems1=nav1.getNavigation()
    #Efems2=nav2.get_Navigation()
    print("Ini")
    Efems=Efems1
    print("Fin")
    Obs=rin.getObservation(['C1'])
    #sat=Satellite_Positioning(Efems,Obs).get_Position()
#     for i in sat:
#         print(i)
#         input()
    sat=SatPositioning(Efems,Obs)
    cab_gps=rin.getHeader()
    sat.getPosition()
#     x=cab_gps["X"]
#     y=cab_gps["Y"]
#     z=cab_gps["Z"]
#     sat.plot_Satellite(pt3.Punto3D(x,y,z))


if __name__=="__main__":
    main()
        
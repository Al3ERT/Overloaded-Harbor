import numpy as np
import math
from Utiles import *


#cantidad de iteraciones del algoritmo que se van a realizar para promediar sus resultados
M=100
#cantidad de salidas de barcos por las que el algoritmo va a esperar antes de devolver el resultado
N = 30

i=0
results=[]
results2=[]
ArribosTotal=0
while i < M:
    arribos = []
    salidas = []
    muelles = [0,0,0]
    Tiempo = 0
    Tiempoarribo = Tiempo + Exponencial(1/8)
    TiempoMuelle1 = np.inf
    TiempoMuelle2 = np.inf
    TiempoMuelle3 = np.inf
    TiempoRemolcador = np.inf
    Remolcador1 = Remolcador()
    Arribos=0
    Salidas = 0
    Recogidos=0
    TiempoEspera = 0
    Esperamuelle=0

    while Salidas<N:
        if Tiempoarribo==min(Tiempoarribo,TiempoMuelle1,TiempoMuelle2,TiempoMuelle3,TiempoRemolcador):
            Tiempo=Tiempoarribo
            Arribos+=1
            if Remolcador1.remolcadoresperando and not Remolcador1.remolcadorenmuelle:
                TiempoRemolcador=Tiempo
            arribos.append(NuevoBarco(Tiempo))
            Tiempoarribo = Tiempo + Exponencial(1/8)

        if TiempoMuelle1 == min(Tiempoarribo,TiempoMuelle1,TiempoMuelle2,TiempoMuelle3,TiempoRemolcador):
            Tiempo=TiempoMuelle1
            if Remolcador1.remolcadoresperando and Remolcador1.remolcadorenmuelle:
                TiempoRemolcador=Tiempo
            muelles[0].Tiempomuelle=Tiempo
            salidas.append(muelles[0])
            TiempoMuelle1=np.inf

        if TiempoMuelle2 == min(Tiempoarribo, TiempoMuelle1, TiempoMuelle2, TiempoMuelle3, TiempoRemolcador):
            Tiempo = TiempoMuelle2
            if Remolcador1.remolcadoresperando and Remolcador1.remolcadorenmuelle:
                TiempoRemolcador=Tiempo
            muelles[1].Tiempomuelle = Tiempo
            salidas.append(muelles[1])
            TiempoMuelle2=np.inf

        if TiempoMuelle3 == min(Tiempoarribo, TiempoMuelle1, TiempoMuelle2, TiempoMuelle3, TiempoRemolcador):
            Tiempo = TiempoMuelle3
            if Remolcador1.remolcadoresperando and Remolcador1.remolcadorenmuelle:
                TiempoRemolcador=Tiempo
            muelles[2].Tiempomuelle = Tiempo
            salidas.append(muelles[2])
            TiempoMuelle3=np.inf

        if TiempoRemolcador == min(Tiempoarribo, TiempoMuelle1, TiempoMuelle2, TiempoMuelle3, TiempoRemolcador):
            Tiempo = TiempoRemolcador
            #Si el remolcador llego al muelle
            if Remolcador1.remolcadorenmuelle:
                #Colocando el barco en un muelle
                if Remolcador1.Barco != None:
                    barco = Remolcador1.Barco
                    Remolcador1.Barco=None
                    count = len(muelles)
                    if muelles[0] == 0:
                        barco.Muelle = 0
                        muelles[0]=barco
                        TiempoMuelle1 = Tiempo+barco.Demora()
                    elif muelles[1] == 0:
                        barco.Muelle = 1
                        muelles[1] = barco
                        TiempoMuelle2 = Tiempo + barco.Demora()
                    elif muelles[2] == 0:
                        barco.Muelle = 2
                        muelles[2] = barco
                        TiempoMuelle3 = Tiempo + barco.Demora()
                if len(salidas)!= 0:
                    barco = salidas.pop(0)
                    Remolcador1.Barco=barco
                    Recogidos+=1
                    Esperamuelle+=Tiempo-barco.Tiempomuelle
                    muelles[barco.Muelle]=0
                    Remolcador1.remolcadorenmuelle = False
                    Remolcador1.remolcadoresperando = False
                    TiempoRemolcador = Tiempo + Exponencial(1)
                elif len(arribos) != 0 and (muelles[0]==0 or muelles[1]==0 or muelles[2]==0):
                    Remolcador1.remolcadorenmuelle = False
                    Remolcador1.remolcadoresperando = False
                    TiempoRemolcador = Tiempo+Exponencial(0.25)
                elif muelles[0]!=0 or muelles[1]!=0 or muelles[2]!=0:
                    Remolcador1.remolcadorenmuelle = True
                    Remolcador1.remolcadoresperando = True
                    TiempoRemolcador = np.inf
                else:
                    Remolcador1.remolcadorenmuelle = False
                    Remolcador1.remolcadoresperando = False
                    TiempoRemolcador = Tiempo+Exponencial(0.25)
            #Si el remolcador llego al puerto
            else:
                if Remolcador1.Barco != None:
                    barco = Remolcador1.Barco
                    TiempoEspera += Tiempo-barco.Tiempollegada
                    Remolcador1.Barco=None
                    Salidas+=1
                if len(arribos)!=0:
                    Remolcador1.Barco=arribos.pop(0)
                    Remolcador1.remolcadorenmuelle=True
                    Remolcador1.remolcadoresperando=False
                    TiempoRemolcador=Tiempo+Exponencial(2)
                else:
                    Remolcador1.remolcadorenmuelle=False
                    Remolcador1.remolcadoresperando=True
                    TiempoRemolcador=np.inf
    ArribosTotal+=Arribos
    results.append(TiempoEspera/Salidas)
    results2.append(Esperamuelle/Recogidos)
    i+=1
count=0
for x in results:
    count+=x
print("Promedio de espera total: "+str(count/M))
count=0
for x in results2:
    count+=x
print("Promedio de espera en el muelle: "+str(count/M))
print("Promedio de arribos: "+str(ArribosTotal/M))
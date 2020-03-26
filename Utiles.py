import numpy as np
import math

def Exponencial(lanbda):
    u = np.random.random()
    while u == 0.0:
        u = np.random.random()

    return -(1 / lanbda) * math.log(u)
def Normal(media,varianza):
    Z = 0
    while 1:
        Y1 =  Exponencial(1)
        Y2 = Exponencial(1)
        Y= Y2 - ((Y1-1)**2)/2
        if Y  > 0:
            if np.random.random()<= 0.5:
                Z= Y1
                break
            else:
                Z=-Y1
                break
    return abs( media + (varianza**(1/2))*Z)

class Barco:
    Tiempollegada = 0
    Muelle = -1
    Tiempomuelle=-1
    def Demora(self):
        return 0
class GranBarco(Barco):
    def Demora(self):
        return Normal(18,3)
class MedBarco(Barco):
    def Demora(self):
        return Normal(12,2)
class PeqBarco(Barco):
    def Demora(self):
        return Normal(9,1)
class Remolcador:
    Barco = None
    remolcadorenmuelle =  False
    remolcadoresperando = True

def NuevoBarco( tiempo):
    a = np.random.random()
    b = Barco()
    if a < 0.25:
        b = PeqBarco()
    elif a < 0.5:
        b = MedBarco()
    else:
        b = GranBarco()
    b.Tiempollegada=tiempo
    return b

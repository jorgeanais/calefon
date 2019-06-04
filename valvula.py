import numpy as np
import hidro
import senal


def gama(D):
    eta = 1.0e2  # Viscosidad del agua en N*s/m² a 20°C
    return 6. * np.pi * D * 0.5 * eta


def presionCamara(caudal):
    Cd = .8  # coef. de descarga
    diametro = 0.01  # diametro del agujero
    densidad = 1000.  # densidad del agua
    area = np.pi * np.power(diametro * .5, 2)
    return 0.5 * np.power(caudal / (Cd * area), 2) * densidad


# Funcion Fd(t)
def Fp(t):
    """
    Fuerza producida por la diferencia de presión en la valvula de agua
    """
    vueltas = senal.rampa(t)
    Dx = hidro.desplazamientoLlave(vueltas)
    area = hidro.area(Dx)
    perdida = hidro.perdidapresionporcarga(10.)
    # Calculo del caudal
    caudal = hidro.caudal(area, 147000-perdida-101000)
    return presionCamara(caudal) * np.pi * np.power(0.01, 2)


def ecdiff(y, t, m, gama, k):
    """
    ODE para el movimiento del eje dentro de la vávula
    """
    x, v = y
    dydt = [v, - k/m * x - gama * v + Fp(t)]
    return dydt

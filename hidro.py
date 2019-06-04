import numpy as np
import senal


def caudal(area, dif_presion):
    """
    Calculo del caudal a través de una llave
    """
    cd = .8  # coeficiente de descarga, adimensional
    dens_agua = 1000.  # densidad del agua en kg/m³
    return cd * area * np.sqrt(2. * dif_presion / dens_agua)


def area(x):
    """
    Calculo del area de paso a través de una llave.
    """
    d_max = .015  # diámetro mayor goma
    d_min = .005  # diámetro menor goma
    h = .01  # altura goma
    return np.pi * np.power((d_max - d_min) / (2*h), 2) * np.power(x, 2)


def desplazamientoLlave(nvueltas):
    """
    Desplazamiento vertical de la goma de la llave en función
    del numero de vueltas.
    """
    paso = 0.001  # paso por vuelta, m.
    return nvueltas * paso


def perdidapresionporcarga(Le):
    """
    Calculo de la diferencia de presión por pérdidas dado un largo de cañería,
    dado la longitud equivalente.
    """
    diam_tub = 0.02   # diametro tubería en m
    q_est = 2.67e-4  # caudal estimado en m³/s
    dens_agua = 1000.  # densidad del agua en kg/m³
    viscosidad = 1.02e-6  # viscosidad cinemática del agua a 20°C, m²/s
    rugosidad = 0.00005    # rugosidad de la tubería
    Lc = diam_tub  # Longitud característica tubería cilíndrica
    area = np.pi * np.power(diam_tub/2., 2)
    v = q_est / area      # velocidad fluido en m/s
    # print(f"v = {v}")
    eD = rugosidad / diam_tub  # factor ε/D
    Re = v * Lc / viscosidad   # numero de Reynolds
    # print(f"ε/D = {eD}")
    # print(f"Re = {Re}")
    fD = 0.035  # factor de fricción (ε/D=0.25, Re=5100), Diagrama Moody
    return fD * .5 * dens_agua * np.power(v, 2) * Le / diam_tub


def longitudequivalente(l0, ncodos):
    """
    Determinación longitud equivalente tubería de acuerdo con el
    número de codos rectos.
    """
    return l0 + 0.3 * ncodos

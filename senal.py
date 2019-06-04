import numpy as np
from scipy import signal


def rampa(t):
    # Definición de la función input
    T = 30  # Periodo en segundos
    nmax = 10.  # nvueltas maximo
    omega = 1. / T
    if t < 30:
        return nmax * 0.5*(signal.sawtooth(2 * np.pi * omega * t) + 1.)
    return 10


def rampavec(t):
    # Definición de la función input
    T = 30  # Periodo en segundos
    nmax = 10.  # nvueltas maximo
    omega = 1. / T
    output = np.zeros(t.size) + nmax
    output[np.where(t < 30)] = nmax * 0.5 * (signal.sawtooth(2 * np.pi * omega * t[np.where(t < 30)]) + 1.)
    return output


# IDEA
def rampa2(t):
    # Definición de la función input
    T = 30  # Periodo en segundos
    nmax = 10.  # nvueltas maximo
    omega = 1. / T
    if t < 30:
        output = nmax * 0.5*(signal.sawtooth(2 * np.pi * omega * t) + 1.)
    elif t > 60 and t < 300:
        output = nmax
    elif t > 300 and t < 330:
        output = (1 - (0.5*(signal.sawtooth(2 * np.pi * omega * t) + 1.)))*nmax
    else:
        output = 0
    return output


def rampavec2(t):
    # Definición de la función input
    T = 30  # Periodo en segundos
    nmax = 10.  # nvueltas maximo
    omega = 1. / T
    output = np.zeros(t.size) + nmax
    output[np.where(t < 30)] = nmax * 0.5*(signal.sawtooth(2 * np.pi * omega * t[np.where(t < 30)]) + 1.)
    output[np.where(t > 300)] = nmax *(1-(0.5*(signal.sawtooth(2 * np.pi * omega * t[np.where(t > 300)]) + 1.)))
    output[np.where(t > 330)] = 0.
    return output

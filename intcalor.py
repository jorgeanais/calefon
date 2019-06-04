import numpy as np
import scipy.interpolate as interpolate


def mpunto(x):
    """
    Flujo de masa (kg/s) que pasa a través de la válvula de gas
    """
    Cd = 0.8  # coef. de descarga
    beta = 0.001 / 0.02  # razón d/D
    e = 0.6  # factor de expansión
    rho = 0.67  # densidad metano kg/m³
    P = 2800  # presión gas en Pa
    dmax = 0.01
    dmin = 0.002
    h = 0.012
    area = np.pi * np.power(0.5*(dmax - dmin)/h, 2) * np.power(x, 2)
    return Cd / np.sqrt(1 - np.power(beta, 4)) * e * np.sqrt(2*rho*P) * area


def calor(mpunto):
    """
    Cantidad de calor entregada al sistema producto de la combustión
    """
    eficiencia = 0.75
    return eficiencia * 50000 * mpunto


def q1(x):
    """
    Función auxiliar para componer mpunto y calor
    """
    return calor(mpunto(x))


def eqconvec(y, t, time, x):
    """
    Ecuación diferencial para modelar la convección de aire en la cámara
    de combustión.
    """
    area = 2 * 0.35 * 0.5 + 2 * 0.5 * 0.16  # area de la camara de combustion
    L = 0.5  # distancia fuente de calor-raidador m
    k = 0.024  # conductividad térmica W/(m·K)
    R = L / (area * k)
    dens = 1.225   # densidad del aire kg / m³
    vol = 0.35 * 0.25 * 0.16  # volumen de la camara de combustion
    m = dens * vol
    c = 1012.  # calor específico del aire en J·kg⁻¹·K⁻¹
    C = m * c
    T0 = 20.  # temp ambiental  en °C
    # Se iterpola para encontrar el valor de x a partir de t
    f = interpolate.interp1d(time, x, bounds_error=False, fill_value=.0)
    dydt = -y/(R*C) + T0/(R*C) + q1(f(t))/(C*(100*(1-np.exp(-t/250)) + 0.01))
    return dydt


def eqconduc(y, t, time, caudal, temp):
    """
    Ecuación diferencial para modelar la conducción del calor desde
    el radiador hacia el agua
    """
    # http://help.solidworks.com/2011/spanish/SolidWorks/cworks/LegacyHelp/Simulation/AnalysisBackground/ThermalAnalysis/Convection_Topics/Convection_Heat_Coefficient.htm
    h = 372.  # coef. de intercambio de calor del cobre en W/(m²K)
    Rt = 0.02  # radio tuberia en m
    cp = 4175.  # calor específico del agua a 35°C en J·kg⁻¹·K⁻¹
    dens_agua = 1000  # densidad del agua kg/m³
    mdot = interpolate.interp1d(time, caudal * dens_agua, bounds_error=False,
                                fill_value=.0)
    Ts = interpolate.interp1d(time, temp, bounds_error=False, fill_value=.0)
    dydx = 2 * np.pi * Rt * h / (mdot(t) * cp) * (Ts(t) - y)
    return dydx

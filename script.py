import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import valvula
import intcalor
import hidro
import senal
# %load_ext autoreload
# %autoreload 2

# tiempo entre 0 y 60 segundos, 10000 muestras.
t = np.linspace(0.1, 600., 60000)

# Condiciones iniciales pos y vel masa-resorte
y0 = [0., 0.]

# Parámetros
m = 0.4  # masa kg
gama = valvula.gama(0.05)
k = 400.  # constante del resorte

sol = odeint(valvula.ecdiff, y0, t, args=(m, gama, k))
x = sol[:, 0]

# Condiciones iniciales T_0 y dT/dt_0
y0 = 20.  # temperatura inicial del aire
time = t
Tradiador = odeint(intcalor.eqconvec, y0, t, args=(time, x))
Tradiador = Tradiador.reshape((-1,))

# Condiciones iniciales T_0 y dT/dt_0
y0 = 20.  # temperatura inicial del agua
time = t

vueltas = senal.rampavec(t)

DeltaX = hidro.desplazamientoLlave(vueltas)
area = hidro.area(DeltaX)
perdida = hidro.perdidapresionporcarga(10.)
caudal = hidro.caudal(area, 147000-perdida-101000)

Tagua = odeint(intcalor.eqconduc, y0, t, args=(time, caudal, Tradiador))


# Plots
plt.plot(t, vueltas, 'c', label='vueltas')
plt.legend(loc='best')
plt.ylabel('Número de vueltas')
plt.xlabel('Tiempo (s)')
plt.grid()
plt.title("Vueltas llave de paso de agua")
plt.show()

plt.plot(t, caudal, 'm', label='Caudal')
plt.legend(loc='best')
plt.ylabel('Caudal ($m^3/s$)')
plt.xlabel('Tiempo (s)')
plt.grid()
plt.title("Caudal de agua en función del tiempo")
plt.show()

plt.plot(t, x, 'g', label='$\Delta x(t)$')
plt.legend(loc='best')
plt.xlabel('tiempo (s)')
plt.ylabel('Posición (m)')
plt.grid()
plt.title("Posición del eje de la válvula")
plt.show()

plt.plot(t, Tradiador, 'r', label='T radiador')
plt.plot(t, Tagua, 'b', label='T agua')
plt.legend(loc='best')
plt.xlabel('tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.grid()
plt.title("Comparación temperaturas radiador y agua")
plt.show()

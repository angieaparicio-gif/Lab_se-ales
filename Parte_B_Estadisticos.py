#Importamos librerias
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew, kurtosis
#Función que permite abrir el archivo .txt
def abrir_archivo_txt(nombre_arch):
    try:
        datos = np.loadtxt(nombre_arch)
    except:
        datos = np.genfromtxt(nombre_arch, skip_header=1)
    if len(datos.shape) > 1:
        datos = datos[:, -1]
    return datos
#Extraemos los valores de voltaje del archivo y los convertimos en flotante para su procesamiento
datos_txt = abrir_archivo_txt('senal.txt')
signal_txt = datos_txt.astype(float)
#Calculamos los estadisticos de la señal
media_txt = np.mean(signal_txt)
disp_txt = np.std(signal_txt, ddof=1)
coe_variacion_txt = np.abs((disp_txt / media_txt) * 100)
asim_txt = skew(signal_txt, bias=False)
curtosis_txt = kurtosis(signal_txt, bias=False)
Cv_inv_txt = 1 / (coe_variacion_txt / 100)
SNR_txt = 20*np.log10(Cv_inv_txt)
#  Imprimimos los estadísticos de la señal
print("ESTADISTICOS senal.txt")
print("Media:", media_txt)
print("Dispersion:", disp_txt)
print("Coeficiente variacion:", coe_variacion_txt)
print("Asimetria:", asim_txt)
print("Curtosis:", curtosis_txt)
print("Relacion señal-ruido:", SNR_txt)
print("\n")
# Graficamos la señal
plt.figure(figsize=(12,6))
plt.plot(signal_txt, linewidth=0.5)
plt.title('Señal - senal.txt')
plt.xlabel('Tiempo (ms)')
plt.ylabel('Amplitud (mV)')
plt.grid(True, alpha=0.3)
#Imprimimos el Histograma Amplitud vs Densidad de probabilidad
plt.figure(figsize=(10,6))                                    
plt.hist(signal_txt, bins=50, density=True)
plt.title('Histograma - senal.txt')
plt.xlabel('Amplitud (mV)')
plt.ylabel('Densidad de probabilidad (mV^(-1))')  
plt.grid(True, alpha=0.3)
plt.axvline(media_txt, linestyle='--')


plt.show()

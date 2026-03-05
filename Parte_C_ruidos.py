import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew, kurtosis
##Función que permite abrir el archivo .txt
def abrir_archivo_txt(nombre_arch):
    try:
        datos = np.loadtxt(nombre_arch)
    except:
        datos = np.genfromtxt(nombre_arch, skip_header=1)
    if len(datos.shape) > 1:
        datos = datos[:, -1]
    return datos
##Definición de variables para el cálculo manual de valores estadísticos
media_manual = 0
N = 0
resta_cuadrada = 0
resta_cubica = 0
resta_4 = 0

datos_txt = abrir_archivo_txt('senal.txt')
signal_txt = datos_txt.astype(float)

media_txt = np.mean(signal_txt)
disp_txt = np.std(signal_txt, ddof=1)
coe_variacion_txt = np.abs((disp_txt / media_txt) * 100)
asim_txt = skew(signal_txt, bias=False)
curtosis_txt = kurtosis(signal_txt, bias=False)

Cv_inv_txt = 1 / (coe_variacion_txt / 100)
SNR_txt = 20*np.log10(Cv_inv_txt)
##  Imprimir estadísticos de la señal .txt 
print("ESTADISTICOS senal.txt")
print("Media:", media_txt)
print("Dispersion:", disp_txt)
print("Coeficiente variacion:", coe_variacion_txt)
print("Asimetria:", asim_txt)
print("Curtosis:", curtosis_txt)
print("Relacion señal-ruido:", SNR_txt)
print("\n")
## Imprimir señal archivo .txt
plt.figure(figsize=(12,6))
plt.plot(signal_txt, linewidth=0.5)
plt.title('Señal - senal.txt')
plt.xlabel('Tiempo (ms)')
plt.ylabel('Amplitud (mV)')
plt.grid(True, alpha=0.3)
## Imprimir Histograma Amplitud vs Densidad de probabilidad
plt.figure(figsize=(10,6))                                    
plt.hist(signal_txt, bins=50, density=True)
plt.title('Histograma - senal.txt')
plt.xlabel('Amplitud (mV)')
plt.ylabel('Densidad de probabilidad (mV^(-1))')  
plt.grid(True, alpha=0.3)
plt.axvline(media_txt, linestyle='--')
## Función para el cálculo de la relación señal ruido (SNR)
def calcular_snr(signal_original, signal_ruidosa):
    potencia_signal = np.mean(signal_original**2)
    potencia_ruido = np.mean((signal_original - signal_ruidosa)**2)
    snr = 10 * np.log10(potencia_signal / potencia_ruido)
    return snr
signal_original = signal_txt
sigma = 10
ruido_gauss = np.random.normal(0, sigma, len(signal_original))
signal_gauss = signal_original + ruido_gauss
snr_gauss = calcular_snr(signal_original, signal_gauss)
print("SNR Ruido Gaussiano (.txt):", snr_gauss, "dB")

plt.figure(figsize=(12,6))
plt.plot(signal_gauss, linewidth=0.5)
plt.title('Señal con Ruido Gaussiano - senal.txt')
plt.xlabel('Tiempo (ms)')
plt.ylabel('Amplitud (mV)')
plt.grid(True, alpha=0.3)

signal_impulso = signal_original.copy()
probabilidad = 0.01
indices = np.random.rand(len(signal_original)) < probabilidad
signal_impulso[indices] = np.max(signal_original) * 3
snr_impulso = calcular_snr(signal_original, signal_impulso)
print("SNR Ruido Impulso (.txt):", snr_impulso, "dB")

plt.figure(figsize=(12,6))
plt.plot(signal_impulso, linewidth=0.5)
plt.title('Señal con Ruido Impulso - senal.txt')
plt.xlabel('Tiempo (ms)')
plt.ylabel('Amplitud (mV)')
plt.grid(True, alpha=0.3)

fs = 400
t = np.arange(len(signal_original)) / fs
frecuencia_artefacto = 0.5
artefacto = 50 * np.sin(2 * np.pi * frecuencia_artefacto * t)
signal_artefacto = signal_original + artefacto
snr_artefacto = calcular_snr(signal_original, signal_artefacto)
print("SNR Ruido Artefacto (.txt):", snr_artefacto, "dB")

plt.figure(figsize=(12,6))
plt.plot(signal_artefacto, linewidth=0.5)
plt.title('Señal con Ruido Artefacto - senal.txt')
plt.xlabel('Tiempo (ms)')
plt.ylabel('Amplitud (mV)')
plt.grid(True, alpha=0.3)


plt.show()

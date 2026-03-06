import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew, kurtosis#importar librerias
#Funciones
def abrir_archivo(nombre_arch, dtype=np.int16):
    with open(nombre_arch, 'rb') as f:
        datos = np.fromfile(f, dtype=dtype)
    return datos
def graficar_senal(datos_graf): #funcion para graficar señal 
    plt.figure (figsize=(12,6))
    plt.plot(datos_graf, linewidth=0.5)
    plt.title ('ECG')
    plt.xlabel('Tiempo (ms)')
    plt.ylabel('Amplitud (mV)')
    plt.axis([0,3000,-50, 150])
    plt.grid(True, alpha = 0.3)
def estadisticos (data, encabezado): #funcion para calcular datos estadisticos
    media_manual = 0
    N = 0
    resta_cuadrada = 0 
    resta_cubica = 0
    resta_4 = 0
    signal = data.astype(float) #Se convierten a float para poder computarizarlos
    for m in signal: 
        media_manual += m
        N = N+1
    media_manual = media_manual / N
    for n in signal:
        #dispersion manual
        resta = n - media_manual
        resta_cuadrada = resta_cuadrada + resta**2
        #Asimetria manual
        resta_cubica = resta_cubica + resta**3
        #Curtosis manual
        resta_4 = resta_4 + resta**4
    #Estadisticos manuales
    dispersion_man = np.sqrt((1/(N-1))*resta_cuadrada)#desviacion estandar
    coe_variacion_man = np.abs((dispersion_man/media_manual) * 100)#coeficiente de variacion 
    asim_man = ((1/N)*resta_cubica) / (dispersion_man**3)#asimetria
    curtosis_man = (((1/N)*resta_4)/(dispersion_man**4)) - 3 #curtosis
    #Estadisticos por funcion
    media = np.mean (data)#media
    disp = np.std(data, ddof =1) #desviacion estandar
    coe_variacion = np.abs((disp / media)*100) #coeficiente de variacion
    asim = skew (data, bias = False) #asimetria
    curtosis = kurtosis(data, bias = False)#curtosis
    Cv_inverso = coe_variacion /100#relacion señal ruido 
    Cv_inverso = 1 / Cv_inverso 
    SNR = 20*np.log10(Cv_inverso)
    print (f"-----ESTADISTICOS {encabezado}------")#impresion de resultados
    print ("Media calculada manualmente: ", media_manual, "\n")
    print ("Media calculada mediante funciones: ", media, "\n")
    print ("Dispersion calculada manualmente: ", dispersion_man, "\n")
    print ("Dispersion calculada mediante funciones: ", disp, "\n")
    print ("Coeficiente de variacion calculado manualmente: ", coe_variacion_man, "\n")
    print ("Coeficiente de variacion calculado mediante funciones: ", coe_variacion, "\n")
    print ("Asimetria calculada manualmente: ", asim_man, "\n")
    print ("Asimetria calculada mediante funciones: ", asim, "\n")
    print ("Curtosis calculada manualmente: ", curtosis_man, "\n")
    print ("Curtosis calculada mediante funciones: ", curtosis, "\n")
    print ("Relacion señal-ruido: ", SNR, "\n")
    # Histograma
    plt.figure(figsize=(10,6))
    plt.hist(signal, bins=50, density=True)
    plt.title(f"Histograma {encabezado}")
    plt.xlabel('Amplitud (mV)')
    plt.ylabel('Densidad de probabilidad (mV^(-1))')
    plt.grid(True, alpha=0.3)
    plt.axvline(media, linestyle='--')
#Ejecución
arch_data = abrir_archivo('rec_10.dat')
graficar_senal (arch_data)
estadisticos (arch_data, 'rec_10.dat')

plt.show()


#Importamos las librerias
import serial
import time
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.animation import FuncAnimation
import threading
#Definimos el puerto serial al que se conecta la STM, los bits por segundo que llegan y el numero maximo de puntos almacenados en la grafica.
PORT = "COM11"
BAUDRATE = 115200
MAX_POINTS = 10000
#se crean los buffers para almacenar los datos de tiempo (x) y voltaje medido el ADC (y), evitando perdida de datos
xdata = deque(maxlen=MAX_POINTS) #Tipo deque para que mantenga unicamente los ultimos 10000 datos recibidos, actualizandose constantemente
ydata = deque(maxlen=MAX_POINTS)
#variable para controlar el funcionamiento del programa.
running = True
#definimos el hilo de lectura del serial
def serial_thread():
    global running
    #abrimos el puerto serial
    ser = serial.Serial(PORT, BAUDRATE, timeout=0)  # NON-BLOCKING
    time.sleep(1)
    start = time.time()
    buffer = ""  # buffer de texto para procesar líneas, evitando que la comunicacion se corte
    print("Leyendo ADC...")
    while running:
        now = time.time()
        elapsed = now - start
        # Leer la cantidad de datos disponibles en el serial
        incoming = ser.read(ser.in_waiting).decode(errors="ignore")
        if incoming: #se ejecuta solo si hay algo en el serial
            buffer += incoming
            # dividimos el texto cuando hay saltos de linea
            lines = buffer.split("\n")
            buffer = lines[-1]  # la última queda incompleta para proxima lectura
            for line_raw in lines[:-1]: #revisamos todas las lineas, menos la ultima, eliminamos espacios.
                line_raw = line_raw.strip()
                if line_raw.isdigit(): 
                    adc = int(line_raw) * 3.3 / 4095 # convertimos de bits a voltaje 
                    # Agregamos los datos para la grafica
                    xdata.append(elapsed)
                    ydata.append(adc)
    ser.close()
    print("Lectura finalizada.")
#Creamos el hilo para la ejecucion
t = threading.Thread(target=serial_thread, daemon=True)
t.start()
#Graficamos
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2) #iniciamos una linea
ax.set_ylim(0, 3.3) #delimitamos el rango (y)
#nombramos los ejes 
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Medida ADC (V)")
ax.set_title("Medición en tiempo real")
#declaramos la funcion para actualizar la grafica
def update(frame):
    line.set_data(xdata, ydata) #actualiza los puntos con los datos del buffer
    if xdata:
        ax.set_xlim(max(0, xdata[0]), xdata[-1]) #desplazamos en x cada que se llene el cuadro
    return line,
#Ejecutamos el update cada 20ms y mostramos la grafica
ani = FuncAnimation(fig, update, interval=20)
plt.show()
#damos por terminado el proceso una vez se cierre la ventana emergente, cerrando, a su vez, el hilo
running = False
t.join()


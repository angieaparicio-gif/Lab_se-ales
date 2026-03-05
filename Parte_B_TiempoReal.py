import serial
import time
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.animation import FuncAnimation
import threading
PORT = "COM11"
BAUDRATE = 115200
MAX_POINTS = 10000
xdata = deque(maxlen=MAX_POINTS)
ydata = deque(maxlen=MAX_POINTS)
running = True
def serial_thread():
    global running
    ser = serial.Serial(PORT, BAUDRATE, timeout=0)  # NON-BLOCKING
    time.sleep(1)
    start = time.time()
    buffer = ""  # buffer de texto para procesar líneas
    print("Leyendo ADC...")
    while running:
        now = time.time()
        elapsed = now - start
        # Leer todo lo disponible
        incoming = ser.read(ser.in_waiting).decode(errors="ignore")
        if incoming:
            buffer += incoming
            # procesar líneas completas
            lines = buffer.split("\n")
            buffer = lines[-1]  # la última queda incompleta
            for line_raw in lines[:-1]:
                line_raw = line_raw.strip()
                if line_raw.isdigit():
                    adc = int(line_raw) * 3.3 / 4095 
                    # Datos para gráfico
                    xdata.append(elapsed)
                    ydata.append(adc)
    ser.close()
    print("Lectura finalizada.")
t = threading.Thread(target=serial_thread, daemon=True)
t.start()
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 3.3)
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Medida ADC (V)")
ax.set_title("Medición en tiempo real")
def update(frame):
    line.set_data(xdata, ydata)
    if xdata:
        ax.set_xlim(max(0, xdata[0]), xdata[-1])
    return line,
ani = FuncAnimation(fig, update, interval=40)
plt.show()
running = False
t.join()

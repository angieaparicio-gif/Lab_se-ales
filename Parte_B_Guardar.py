import serial
import time
PORT = "COM11"      
BAUDRATE = 115200
OUTPUT_FILE = "senal_capturada.txt"
CAPTURE_TIME = 4.0     # segundos de muestra
ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)  # Dar tiempo a que el STM32 reinicie
print(f"Capturando datos durante {CAPTURE_TIME} segundos...")
with open(OUTPUT_FILE, "w") as f:
    f.write("timestamp_s\tadc_value\n")  
    start = time.time()
    while True:
        now = time.time()
        elapsed = now - start
        # Parar a los X segundos
        if elapsed >= CAPTURE_TIME:
            print("\n Captura finalizada.")
            break
        line = ser.readline().decode(errors="ignore").strip()
        if line.isdigit():
            adc_value = int(line)
            f.write(f"{elapsed:.6f}\t{adc_value}\n")
            print(f"{elapsed:.3f}s -> {adc_value}")

ser.close()
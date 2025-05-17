import socket
import time
import serial
import threading
from Adafruit_IO import Client

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

TCP_IP = "192.168.0.100"
TCP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

ADAFRUIT_AIO_USERNAME = "taamnguyeen04"
ADAFRUIT_AIO_KEY = "aio_yjdc83QxJOH6zQ8OlKyiNXwUIRQM"
aio = Client(ADAFRUIT_AIO_USERNAME, ADAFRUIT_AIO_KEY)

latest_weight = 0
latest_voltage = 0
lock = threading.Lock()

def read_sensor():
    global latest_weight, latest_voltage
    while True:
        try:
            data = ser.readline().decode().strip()
            if data:
                weight, voltage = map(float, data.split(","))
                with lock:
                    latest_weight = weight
                    latest_voltage = voltage
                print(f"data: {weight} g | {voltage} V")
        except Exception as e:
            print("loi", e)
        time.sleep(0.5)

def send_tcp():
    while True:
        with lock:
            message = f"{latest_weight},{latest_voltage}\n"
        sock.sendall(message.encode())
        print(f"TCP: {message.strip()}")
        time.sleep(1)

def send_adafruit():
    while True:
        with lock:
            weight = latest_weight
            voltage = latest_voltage
        aio.send("SmartCart_01_Weight", weight)
        aio.send("SmartCart_01_Voltage", voltage)
        print(f"Adafruit IO: weight = {weight} g | voltage = {voltage} V")
        time.sleep(5)

thread_sensor = threading.Thread(target=read_sensor)
thread_tcp = threading.Thread(target=send_tcp)
thread_adafruit = threading.Thread(target=send_adafruit)

thread_sensor.start()
thread_tcp.start()
thread_adafruit.start()

thread_sensor.join()
thread_tcp.join()
thread_adafruit.join()

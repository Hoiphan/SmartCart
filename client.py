# import requests

# SERVER_URL = "http://192.168.0.100:8000/logs/"
# DEVICE_ID = "raspi_01"
# data = {
#     "device_id": DEVICE_ID,
#     "status": "alo alo alo..."
# }

# response = requests.post(SERVER_URL, json=data)
# print(response.json())


import socket
import time
import serial

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
TCP_IP = "192.168.0.100"
TCP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

# for i in range(10):
#     message = f"Test {i+1}\n"
#     print(f"?? G?i: {message.strip()}")
#     sock.sendall(message.encode())
#     time.sleep(1)

while True:
    try:
        data = ser.readline().decode().strip()
        if data:
            weight, voltage = map(float, data.split(","))
            message = f"{weight}, {voltage}"
            sock.sendall(message.encode())
            print(f"can nang: {weight} g | volt: {voltage} V")
    except Exception as e:
        print("Error:", e)


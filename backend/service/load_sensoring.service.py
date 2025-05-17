#Tam

import time
import RPi.GPIO as GPIO
from hx711 import HX711

DT_PIN = 5
SCK_PIN = 6

# Khởi tạo HX711
hx = HX711(DT_PIN, SCK_PIN)

def read_weight():
    try:
        val = hx.get_weight(5)
        print(f"Load: {val:.2f} g")
        hx.power_down()
        hx.power_up()
        time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    try:
        while True:
            read_weight()
    except KeyboardInterrupt:
        print("Dừng chương trình")
        GPIO.cleanup()
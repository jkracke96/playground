from classes import Hardware
#from classes import TimeKeeper as TK
import schedule
import smtplib
import time
import ssl
from gpiozero import InputDevice

# WATERING_TIME must be in "00:00:00 PM" format
WATERING_TIME = '11:59:50 AM'
SECONDS_TO_WATER = 10

RELAY = Hardware.Relay(12, False)

SENSOR_PIN = 17
sensor = InputDevice(SENSOR_PIN)

def water_plant(relay, seconds):
    relay.on()
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    relay.off()

def read_sensor():
    soil_moisture = sensor.value
    return soil_moisture

def main():
    while True:
        RELAY.off()
        answer = input("start pump (y/n)?")
        soil_moisture = read_sensor()
        if answer.lower() == 'y' and soil_moisture == 1:
            print(f"Soil moisture sensor reading: {soil_moisture}")
            RELAY.on()
            time.sleep(SECONDS_TO_WATER)


if __name__ == "__main__":
    main()
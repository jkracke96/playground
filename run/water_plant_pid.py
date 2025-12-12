from classes import Hardware
#from classes import TimeKeeper as TK
import schedule
import smtplib
import time
import ssl
from gpiozero import InputDevice, Button
from simple_pid import PID
from signal import pause

# WATERING_TIME must be in "00:00:00 PM" format
WATERING_TIME = '11:59:50 AM'
SECONDS_TO_WATER = 200

RELAY = Hardware.Relay(12, False)

SENSOR_PIN = 17
sensor = InputDevice(SENSOR_PIN)

pid = PID(-1.0, 0.0, 0.0, 0.1)  # setpoint for 50% duty cycle
duty_cycle = 0.1

def water_plant(relay, seconds):
    print("Plant is being watered!")
    start_time = time.time()
    cycle_time = 1.0  # 1 second cycle
    while time.time() - start_time < seconds:
        soil_moisture = sensor.value  # scale to 0-100
        duty_cycle = pid(soil_moisture)  # no feedback from sensor
        on_time = duty_cycle * cycle_time
        off_time = (1 - duty_cycle) * cycle_time
        if on_time < 0:
            break
        relay.on()
        time.sleep(on_time)
        relay.off()
        time.sleep(off_time)
    print("Watering is finished!")

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
            water_plant(RELAY, SECONDS_TO_WATER)
            #RELAY.on()
            #time.sleep(SECONDS_TO_WATER)

def button_pressed():
    print("Button pressed! Starting watering process.")
    time.sleep(2)  # Debounce delay


if __name__ == "__main__":
    main()

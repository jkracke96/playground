from classes import Hardware
#from classes import TimeKeeper as TK
import schedule
import smtplib
import time
import ssl
from gpiozero import InputDevice

class PID:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.previous_error = 0
        self.integral = 0

    def update(self, process_variable):
        error = self.setpoint - process_variable
        self.integral += error
        derivative = error - self.previous_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        return output

# WATERING_TIME must be in "00:00:00 PM" format
WATERING_TIME = '11:59:50 AM'
SECONDS_TO_WATER = 10

RELAY = Hardware.Relay(12, False)

SENSOR_PIN = 17
sensor = InputDevice(SENSOR_PIN)

pid = PID(1.0, 0.0, 0.0, 0.5)  # setpoint for 50% duty cycle

def water_plant(relay, seconds):
    print("Plant is being watered!")
    start_time = time.time()
    cycle_time = 1.0  # 1 second cycle
    while time.time() - start_time < seconds:
        duty_cycle = pid.update(0)  # no feedback from sensor
        on_time = duty_cycle * cycle_time
        off_time = (1 - duty_cycle) * cycle_time
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


if __name__ == "__main__":
    main()
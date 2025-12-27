from classes import Hardware
#from classes import TimeKeeper as TK
import schedule
import smtplib
import time
import ssl
from gpiozero import InputDevice, Button
from simple_pid import PID
from signal import pause
from classes.Hardware import MCP3008
from spidev import SpiDev


RELAY = Hardware.Relay(12, False)
RELAY_AC = Hardware.Relay(21, False)

# CONFIGS
MIN_BREW_TEMP = 90
MAX_BREW_TEMP = 96
MIN_ADC = 0
MAX_ADC = 4096


def brew_coffee():
    while True:
        data = read_sensor()
        brew_temp = (data - MIN_ADC) / (MAX_ADC - MIN_ADC) * (MAX_BREW_TEMP - MIN_BREW_TEMP) + MIN_BREW_TEMP
        print(brew_temp)
        if data > 2000:
            RELAY_AC.on()
            RELAY.off()
        else:
            RELAY.on()
            RELAY_AC.off()
        time.sleep(2)


def read_sensor():
    adc = MCP3008()
    data = adc.read(0)
    adc.close()
    return data


if __name__ == "__main__":
    button = Button(2)
    button.when_pressed = brew_coffee
    pause()
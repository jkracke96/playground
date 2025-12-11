from classes import Hardware
#from classes import TimeKeeper as TK
import schedule
import smtplib
import time
import ssl

# WATERING_TIME must be in "00:00:00 PM" format
WATERING_TIME = '11:59:50 AM'
SECONDS_TO_WATER = 30
RELAY = Hardware.Relay(12, False)

def water_plant(relay, seconds):
    relay.on()
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    relay.off()

def main():
    while True:
        RELAY.off()
        answer = input("start pump (y/n)?")
        if answer.lower() == 'y':
            RELAY.on()
            time.sleep(SECONDS_TO_WATER)


if __name__ == "__main__":
    main()
import RPi.GPIO as GPIO
import sys
import time

###################################################
##   Lights Controller with Configurable inputs  ##
###################################################



GPIO.setmode(GPIO.BCM)

##################################
##   PIN LIGTH DECLARATION      ##
##################################
PIN_KITCHEN = 4
PIN_ROOM = 7
PIN_BATH = 9
PIN_POOL = 10
PIN_EMERGENCYLIGHT = 11


##################################
##   SET UP LIGTH PIN           ##
##################################

GPIO.setup(PIN_ROOM, GPIO.OUT)
GPIO.setup(PIN_BATH, GPIO.OUT)
GPIO.setup(PIN_POOL, GPIO.OUT)
GPIO.setup(PIN_KITCHEN, GPIO.OUT)
GPIO.setup(PIN_EMERGENCYLIGHT, GPIO.OUT)

kitchen = GPIO.PWM(PIN_KITCHEN, 100)
kitchen.start(0)
dc_k = 75
kitchen.ChangeDutyCycle(dc_k)

room = GPIO.PWM(PIN_ROOM, 100)
room.start(0)
dc_r = 50
room.ChangeDutyCycle(dc_r)

bath = GPIO.PWM(PIN_BATH, 100)
bath.start(0)
dc_p = 75
bath.ChangeDutyCycle(dc_p)

emergency = GPIO.PWM(PIN_EMERGENCYLIGHT, 30)
emergency.start(0)

pool = GPIO.PWM(PIN_POOL, 100)
pool.start(0)
while True:
    # Special Effects for swiming-pool led
    for dc_po in range(0, 101, 5):
        pool.ChangeDutyCycle(dc_po)  # Change duty cycle
        time.sleep(0.05)
    time.sleep(1)
    for dc_po in range(100, -1, -5):  # Decrease duty cycle
        pool.ChangeDutyCycle(dc_po)
        time.sleep(0.05)
    time.sleep(1)

##################################
##   SET UP Emergency Alert     ##
##################################

emergencyButton = 2
partyButton = 3
shutDownEmergencyButton = 8
events = [emergencyButton,partyButton,shutDownEmergencyButton]

GPIO.setup(emergencyButton, GPIO.IN, GPIO.PUD_UP)
channel = 'emergency'

def callback(channel):

    if channel == emergencyButton:

        print('Emergency')
        emergency.ChangeDutyCycle(80)   # turn on emergency light

    elif channel == partyButton:
        ## Special effects for all house
        for dc in range(0, 101, 5):
            pool.ChangeDutyCycle(dc)  # Change duty cycle
            bath.ChangeDutyCycle(dc)
            room.ChangeDutyCycle(dc)
            kitchen.ChangeDutyCycle(dc)
            time.sleep(0.05)
        time.sleep(1)
        for dc_po in range(100, -1, -5):  # Decrease duty cycle
            pool.ChangeDutyCycle(dc)
            bath.ChangeDutyCycle(dc)
            room.ChangeDutyCycle(dc)
            kitchen.ChangeDutyCycle(dc)
            time.sleep(0.05)
        time.sleep(1)
    elif channel == shutDownEmergencyButton:
        GPIO.output(PIN_EMERGENCYLIGHT, GPIO.HIGH)




GPIO.add_event_detect(events, GPIO.FALLING,callback=callback)

try:
    while 1:
        pass

except KeyboardInterrupt:
    pool.stop()
    GPIO.output(PIN_KITCHEN, GPIO.HIGH)  # turn off all leds except Emergency
    GPIO.output(PIN_ROOM, GPIO.HIGH)
    GPIO.output(PIN_BATH, GPIO.HIGH)
    GPIO.output(PIN_POOL, GPIO.HIGH)
    GPIO.cleanup()
    sys.exit(1)

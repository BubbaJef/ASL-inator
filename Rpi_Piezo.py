from time import time
import RPi.GPIO as GPIO

#set led and button
switch = 12
led = 13

#set GPIO
GPIO.setwarnings(False)
GPIO.setmore(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
pin7 = GPIO.PWM(7, 100)
pin7.start(50)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)

start = time()
current = time()

while True:
    if GPIO.input(switch) == True:
        current = time()
    else:
        start = time()

    if ((current - start) > 3):
        GPIO.output(led, GPIO.HIGH)
        GPIO.output(7, GPIO.HIGH)
        pin7.ChangeFrequency(440.00) #A4
    else:
        GPIO.output(led, GPIO.LOW)
        GPIO.output(7, GPIO.LOW)

from tkinter import *
from tkinter import font
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from time import time, sleep
import RPi.GPIO as GPIO

led = 13  # GPIO 27 = pin 13
piezo = 7  # GPIO 04 = pin 7

PORT_NUMBER = 5000
SIZE = 1024

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
pin7 = GPIO.PWM(7, 100)
pin7.start(50)
GPIO.setup(led, GPIO.OUT)
start = time()
current = time()

String = ""
Read = ""
is_beeping = False

GPIO.output(7, GPIO.LOW)
pin7.ChangeFrequency(0.1)


def receive_data():
    global String
    global Read
    data, addr = mySocket.recvfrom(SIZE)
    print(data)

    if len(data) > 1:
        String = data
        start = time()
        GPIO.output(led, GPIO.HIGH)
        GPIO.output(7, GPIO.HIGH)
        pin7.ChangeFrequency(300)
        sleep(0.1)  # Beep for 0.1 seconds
        GPIO.output(led, GPIO.LOW)
        GPIO.output(7, GPIO.LOW)
        pin7.ChangeFrequency(0.1)

    else:
        GPIO.output(led, GPIO.LOW)
        GPIO.output(7, GPIO.LOW)
        pin7.ChangeFrequency(0.1)
        if data == "~":
            String = ""
        elif data == "<":
            String = String[:-1]
        Read = data


    confirmed_letter.delete("1.0", END)
    confirmed_letter.insert(END, Read)
    confirmed_letter.tag_add("center", "1.0", "end")
    status_bar1.config(text=String)
    app.after(100, receive_data)

hostName = gethostbyname('0.0.0.0')

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))

app = Tk()
app.bind('<Escape>', lambda e: app.quit())

customFont_2 = font.Font(family='Arial', size=25)

status_bar1 = Label(app, bd=1, relief=SUNKEN, anchor=W, height=2, font=customFont_2)
status_bar1.grid(row=2, column=0, columnspan=2, sticky=E+W)

customFont = font.Font(family='Arial', size=100)

confirmed_letter = Text(app, bd=1, relief=SUNKEN, height=1, width=2, font=customFont)
confirmed_letter.grid(row=0, column=1, padx=10, pady=10, sticky=NE)
confirmed_letter.tag_configure("center", justify='center')

app.after(100, receive_data)

app.mainloop()
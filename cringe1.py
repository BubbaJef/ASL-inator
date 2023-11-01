from tkinter import *
from tkinter import font
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from time import time

PORT_NUMBER = 5000
SIZE = 1024
String = ""
def receive_data():
    data, addr = mySocket.recvfrom(SIZE)
    print(data)

    if (len(data) > 1):
        String = data
    else:
        Read = data
    
    confirmed_letter.delete("1.0", END)
    confirmed_letter.insert(END, data)
    confirmed_letter.tag_add("center", "1.0", "end")
    status_bar1.config(text=data)
    app.after(100, receive_data)  # Schedule the function to run again in 100 milliseconds

hostName = gethostbyname('0.0.0.0')

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))

app = Tk()
app.bind('<Escape>', lambda e: app.quit())

customFont_2 = font.Font(family='Arial', size=25)

# status bar
status_bar1 = Label(app, bd=1, relief=SUNKEN, anchor=W, height=2, font=customFont_2)
status_bar1.grid(row=2, column=0, columnspan=2, sticky=E+W)

customFont = font.Font(family='Arial', size=100)

# status bar
confirmed_letter = Text(app, bd=1, relief=SUNKEN, height=1, width=2, font=customFont)
confirmed_letter.grid(row=0, column=1, padx=10, pady=10, sticky=NE)
confirmed_letter.tag_configure("center", justify='center')

app.after(100, receive_data)  # Start receiving data

app.mainloop()

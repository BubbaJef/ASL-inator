from tkinter import *
from tkinter import font
from time import time
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys

PORT_NUMBER = 5000
SIZE = 1024

hostName = gethostbyname( '0.0.0.0' )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))

app = Tk()
app.bind('<Escape>', lambda e: app.quit())

customFont_2 = font.Font(family = 'Arial',size=25)

#status bar
status_bar1 = Label(app, bd=1, relief=SUNKEN, anchor=W, height=2, font=customFont_2)
status_bar1.grid(row=2, column=0, columnspan=2, sticky=E+W)

customFont = font.Font(family = 'Arial',size=100)

#status bar
confirmed_letter = Text(app, bd=1, relief=SUNKEN, height=1, width=2, font=customFont)
confirmed_letter.grid(row=0, column=1, padx=10, pady=10, sticky=NE)
confirmed_letter.tag_configure("center", justify='center')

data = "-"
String = "Cringe"

def Cringe():
    while True:
        (data,addr) = mySocket.recvfrom(SIZE)
        print(data)
        confirmed_letter.delete("1.0", END)  # Delete current content
        confirmed_letter.insert(END, data)   # Insert the new letter
        confirmed_letter.tag_add("center", "1.0", "end")
        status_bar1.config(text=String)
    

Cringe()    
app.mainloop()
sys.exit()




from tkinter import *
from tkinter import font
from time import time
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys




app = Tk()

app.bind('<Escape>', lambda e: app.quit())

# Make the window fullscreen
app.attributes('-fullscreen', True)

# Create a frame to hold the widgets and make it fill the screen
frame = Frame(app)
frame.pack(expand=True, fill='both')

# Disable the standard window decorations (close, minimize, maximize buttons)


# Allow the window to be closed with the Escape key
app.protocol("WM_DELETE_WINDOW", app.quit)

# Configure grid rows and columns to expand
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Create a frame for the status_bar on the left half of the screen
status_frame = Frame(frame, bd=10, relief=SUNKEN)
status_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
status_frame.grid_rowconfigure(0, weight=1)
status_frame.grid_columnconfigure(0, weight=1)

# Create a status bar label inside the left frame
customFont1 = font.Font(family="Arial", size=80)
status_bar = Label(status_frame, text="Text", anchor=W, font=customFont1, height=3)
status_bar.pack(fill="both", expand=True)

# Create a frame for the confirmed_letter on the right half of the screen
confirmed_frame = Frame(frame, bd=10, relief=SUNKEN)
confirmed_frame.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)
confirmed_frame.grid_rowconfigure(0, weight=1)
confirmed_frame.grid_columnconfigure(0, weight=1)

# Create a Text widget for confirmed letters inside the right frame
customFont = font.Font(family="Arial", size=100)
confirmed_letter = Text(confirmed_frame, bd=10, relief=SUNKEN, height=1, width=2, font=customFont)
confirmed_letter.grid(row=0, column=0, sticky=NSEW)
confirmed_letter.tag_configure("center", justify='center')

app.mainloop()

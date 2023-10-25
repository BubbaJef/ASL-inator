from tkinter import *
import cv2
from PIL import Image, ImageTk

#make constants
WIDTH = 400
HEIGHT = 500

#initiate camera
vid = cv2.VideoCapture(0)

vid.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

app = Tk()

app.bind('<Escape>', lambda e: app.quit())

label_widget = Label(app)
label_widget.pack()

# Status bar
status_bar = Label(app, text="YES", bd=1, relief=SUNKEN, anchor=W)
status_bar.pack(side=BOTTOM, fill=X)

# Vertical Status bar
status_bar = Label(app, text="Reading, Input, queue", bd=1, relief=SUNKEN, anchor=W)
status_bar.pack(side=RIGHT, fill=Y)


def open_camera():
    _, frame = vid.read()

    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    captured_image = Image.fromarray(opencv_image)

    photo_image = ImageTk.PhotoImage(image=captured_image)

    label_widget.photo_image = photo_image

    label_widget.configure(image=photo_image)

    label_widget.after(10, open_camera)

button1 = Button(app, text="Open Camera", command=open_camera)
button1.pack()

app.mainloop()

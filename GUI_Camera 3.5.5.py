from tkinter import *
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import math
from time import time
from tkinter import font

#make constants
WIDTH = 400
HEIGHT = 500

#mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

MYHAND = .07 #set scale of tested hand

#Make constants
DEBUG = False
FIND = False
ID = True
CONFIRM = True

#Confirm og values
global Read
global HasRead
global String
global ReadCount
global NewRead
Read = ""
HasRead = ""
String = ""
ReadCount = 0
NewRead = 0


# Euclidean distance
def compute_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)**0.5

#initiate camera
vid = cv2.VideoCapture(0)

vid.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

app = Tk()

app.bind('<Escape>', lambda e: app.quit())

label_widget = Label(app)
label_widget.pack()

# Status bar
status_bar1 = Label(app, text="YES", bd=1, relief=SUNKEN, anchor=W)
status_bar1.pack(side=BOTTOM, fill=X)

# Vertical Status bar (Text widget for live terminal output)
vertical_status_bar = Text(app, wrap=WORD, height=20, width=30)
vertical_status_bar.pack(side=RIGHT, fill=Y)

# Function to write text to the vertical status bar
def write_to_status_bar(text):
    vertical_status_bar.insert(END, text + '\n')
    vertical_status_bar.see(END)  # Auto-scroll to the end of the text

# Redirect stdout to the vertical status bar
import sys
sys.stdout.write = write_to_status_bar

customFont = font.Font(family = "Arial",size = 100)

#status bar
confirmed_letter = Text(app, bd=1, relief=SUNKEN, height=1, width=2, font=customFont)  # Adjust the height and width accordingly
confirmed_letter.pack(side=TOP, fill=X)  
confirmed_letter.place(relx=1.0, rely=0.0, anchor="ne")
confirmed_letter.tag_configure("center", justify='center')


def open_camera():
    _, frame = vid.read()

    currentTime = time()

    global Read, HasRead, String, ReadCount, NewRead

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

    results = hands.process(frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks on the image
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            #get markers for each point
            Tt = hand_landmarks.landmark[4] #thumb tip
            Pt = hand_landmarks.landmark[20] #pinky tip
            H0 = hand_landmarks.landmark[0] #Hand 0 (wrist)
            Mt = hand_landmarks.landmark[12] #middle tip
            Hi = hand_landmarks.landmark[5] #index start
            Ps = hand_landmarks.landmark[17] #pinky start
            Rt = hand_landmarks.landmark[16] #Ring tip
            It = hand_landmarks.landmark[8] #Index tip
            Ts = hand_landmarks.landmark[2] #Thumb start
            
            z_dist = -10000000*H0.z #set z distance constant
            
            z_scale = round(11/z_dist,2)
            
            #set hand scale
            scale = round((round(compute_distance(H0, Hi)*(z_scale), 2)) * (round(compute_distance(Ps, Hi)*(z_scale), 2)),2)
            

            comp = (round(scale/MYHAND,4))
    
            
            PTdist = abs(round(compute_distance(Pt, Tt)*(z_scale), 2)) #Pinky-Thumb
            HPdist = abs(round(compute_distance(H0, Pt)*(z_scale), 2)) #Wrist-Pinky tip
            HTdist = abs(round(compute_distance(H0, Tt)*(z_scale), 2)) #Wrist-Thumb tip
            HMdist = abs(round(compute_distance(H0, Mt)*(z_scale), 2)) #Wrist-Middle tip
            HRdist = abs(round(compute_distance(H0, Rt)*(z_scale), 2)) #Wrist-Ring tip
            HIdist = abs(round(compute_distance(H0, It)*(z_scale), 2)) #Wrist-Index tip
            HTs_dist = abs(round(compute_distance(H0, Ts)*(z_scale), 2)) #Wrist-Thumb start
            TIdist = abs(round(compute_distance(Ts, It)*(z_scale), 2)) #Thumb start - Index tip
            TtPs_dist = abs(round(compute_distance(Tt, Ps)*(z_scale), 2)) #Thumb tip - Pinky start
            IMdist = abs(round(compute_distance(It, Mt)*(z_scale), 2)) #Middle tip - Index tip
            TRdist = abs(round(compute_distance(Tt, Rt)*(z_scale), 2)) #Thumb tip to Ring Tip
            
            ''' IDENTIFY HANDS '''
            if (ID):
                if ((comp*PTdist) > (.4) and (comp*HMdist < 0.4) and (comp*HPdist > 0.4) and \
                    (comp*HRdist < 0.4) and (comp*HIdist < 0.4) and (comp*TtPs_dist > 0.2)):
                    #print("Y")
                    Read = "Y"

                elif((comp*HRdist < .4) and (comp*HIdist > .4) and (comp*HMdist > .4) \
                    and (HPdist < .4) and (comp < 1.3)):
                    # U or V
                    if (comp*IMdist < 0.1):
                        Read = "U"
                    else:
                        Read = "V"
                
                elif((comp*HRdist < 1.4) and (comp*HIdist < 1.4) and (comp*HMdist < 1.4) \
                    and (HPdist < 1.4) and (comp > 1)):
                    #print("***Fingers Down***")

                    if (comp*TtPs_dist < 0.55):
                        print("Hand Closed")
                            
                        if (comp*TIdist < 0.6) and (comp*TRdist > 0.3):
                            #print("S")
                            Read = "S"

                        elif (comp*TRdist < 0.4):
                            #print("E")
                            Read = "E"

                
                     
                    
                    
                            
                else:
                    Read = "-"                    

                print("")

            if (DEBUG):
                print("")
                print("DEBUG")
                print("PTdist: {} Upper: {} Lower: {}".format((PTdist), comp*(1.1), comp*(.7)))
                print("HTdist: {} Upper: {} Lower: {}".format((HTdist), comp*(0.47), comp*(0.37)))
                print("z: {}".format(z_dist))
                print("% = {}, area = {}".format(comp, scale))
                print("PTdist: {}, HPdist: {}, HTdist: {}, HMdist: {}".format(PTdist, HPdist, HTdist, HMdist))
                print("")

            if (FIND):
                print("")
                print("FIND:")
                print("% = {}, scale = {}".format(comp, scale))
                #print("PT:{}, HM:{}, HR:{}, HI:{}".format(PTdist, HMdist, HRdist, HIdist))  #for 'y'
                #print("HTdist:{}, HTs_dist:{}, TIdist:{}".format(HTdist, HTs_dist, TIdist))
                print("HP: {}, HR: {}, HM: {}, HI: {}, HT{}".format(HPdist, HRdist, HMdist, HIdist, HTdist))
                print("TtPs_dist: {}, IMdist: {}".format(TtPs_dist, IMdist))
                print("TRdist: {}, TIdist: {}".format(TRdist, TIdist))
                print("")
                pass

            print("Read: {}".format(Read))

            if (CONFIRM):            
                if (NewRead > 10):
                    HasRead = Read
                    NewRead = 0
                    print("New letter!")
                    
                if (Read == HasRead):
                    ReadCount += 1 
                    NewRead -= 1
                    
                    if (NewRead < 0):
                        NewRead = 0
                        
                else:
                    ReadCount -= 1
                    NewRead += 1

                    if (ReadCount < 0):
                        ReadCount = 0

                if ((ReadCount > 20) and (Read != "-") and ((currentTime - markTime) > 3)):
                    print("Confirm Letter: {}".format(Read))
                    markTime = time()
                    NewRead = 0
                    ReadCount = 0
                    String += Read
    
    
    status_bar1.config(text=String)

    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    captured_image = Image.fromarray(opencv_image)

    photo_image = ImageTk.PhotoImage(image=captured_image)

    label_widget.photo_image = photo_image

    label_widget.configure(image=photo_image)

    label_widget.after(10, open_camera)

button1 = Button(app, text="Open Camera", command=open_camera)
button1.pack()

app.mainloop()

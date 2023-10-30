import cv2
import mediapipe as mp
import math
from time import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

MYHAND = .07 #set scale of tested hand

#Make constants
DEBUG = False
FIND = False
ID = True
CONFIRM = True

#Confirm og values
Read = ""
HasRead = ""
String = ""
ReadCount = 0
NewRead = 0
markTime = time()

# Euclidean distance
def compute_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)**0.5

hands = mp_hands.Hands()

cap = cv2.VideoCapture(1)

while cap.isOpened():

    currentTime = time()
    
    #get video
    ret, image = cap.read()
    #flip image
    image = cv2.flip(image, 1)
    if not ret:
        continue
    
    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks on the image
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            '''Acess Points'''
            Tt = hand_landmarks.landmark[4] #thumb tip
            Pt = hand_landmarks.landmark[20] #pinky tip
            H0 = hand_landmarks.landmark[0] #Hand 0 (wrist)
            Mt = hand_landmarks.landmark[12] #middle tip
            Hi = hand_landmarks.landmark[5] #index start
            Ps = hand_landmarks.landmark[17] #pinky start
            Rt = hand_landmarks.landmark[16] #Ring tip
            It = hand_landmarks.landmark[8] #Index tip
            Ts = hand_landmarks.landmark[2] #Thumb start
            In = hand_landmarks.landmark[6] #Index Nuckle
            H1 = hand_landmarks.landmark[1] #Hand 1 (Thumb Pad)
            
            
            z_dist = -10000000*H0.z #set z distance constant
            
            z_scale = round(11/z_dist,2)
            
            #set hand scale
            scale = round((round(compute_distance(H0, Hi)*(z_scale), 2)) * (round(compute_distance(Ps, Hi)*(z_scale), 2)),2)
            

            comp = (round(scale/MYHAND,4))
    
            '''Get Distances'''
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
            TtIsdist = abs(round(compute_distance(Tt, Hi)*(z_scale), 2)) #Thumb tip - Index start
            
            ''' IDENTIFY HANDS '''
            if (ID):
                #if ((comp*PTdist) > (.4) and (comp*HMdist < 0.4) and (comp*HPdist > 0.4) and \
                    #(comp*HRdist < 0.4) and (comp*HIdist < 0.4) and (comp*TtPs_dist > 0.2) and (Tt.y < In.y)):
                    #print("Y")
                    #Read = "Y"

                if ((Ps.y > H1.y) and (It.y < H0.y)):
                    if ((Mt.x < In.x) and (Rt.x < In.x) and (Pt.x < In.x) and (It.x > In.x)):
                        if (Tt.y < It.y):
                            Read = "G"
                        else:
                            Read = "P"
                    elif ((Mt.x > In.x) and (Rt.x < In.x) and (Pt.x < In.x) and (It.x > In.x)):
                        Read = "H"
                    
                elif ((Mt.y > Hi.y) and (Rt.y > Hi.y) and (Pt.y > Hi.y) and (It.y < Hi.y) and (It.y < H0.y)):
                    if (Tt.x > Hi.x):
                        if (It.y > In.y):
                            Read = "X"
                        elif (Tt.y > Rt.y):
                            Read = "D"
                        elif (Tt.y < Rt.y):
                            Read = "Z"
                    elif ((Tt.x < Hi.x)  and (comp*TtIsdist > 0.7)):
                        Read = "L"
                    else:
                        "-"
                    
                elif ((Mt.y < In.y) and (Rt.y < In.y) and (Pt.y > In.y) and (It.y < In.y)\
                      and (Tt.x > Mt.x) and (It.y < H0.y)):
                    Read = "W"

                elif ((Mt.y < In.y) and (Rt.y < In.y) and (Pt.y < In.y) and (It.y > In.y) \
                      and (Tt.y > Hi.y) and (It.y < H0.y)):
                     Read = "F"
                     
                elif ((Mt.y < In.y) and (Rt.y < In.y) and (Pt.y < In.y) and (It.y < In.y) \
                      and (Tt.y > Hi.y) and (Tt.x > Mt.x)):
                     Read = "B"

                elif ((Mt.y > In.y) and (Rt.y > In.y) and (Pt.y < In.y) and (It.y > In.y) and (It.y < H0.y)):
                    if ((Tt.y > In.y) and (Tt.x > Hi.x) and (Tt.x < Rt.x)):
                        Read = "J"
                    elif ((Tt.y > In.y) and (Tt.x < Hi.x)):
                        Read = "I"
                    elif ((comp*TtPs_dist > 0.2) and (Tt.y < In.y) and (comp*PTdist) > (.4)):
                        Read = "Y"                  
                    
                elif((It.y < Hi.y) and (Pt.y > Ps.y) and (It.y < H0.y)):
                    if ((Mt.y < Hi.y) and (Rt.y > Ps.y)): 
                        # U, V, R, K, '''H'''
                        if (It.x > Mt.x):
                            Read = "R"
                        elif (comp*IMdist < 0.1):
                            Read = "U"
                        elif ((Tt.x > It.x) and (Tt.y < Hi.y)):
                            Read = "K"
                        elif (comp*IMdist > 0.1):
                            Read = "V"
                            
                elif((Pt.y > Hi.y) and (Rt.y > Hi.y) and (Mt.y > Hi.y) \
                    and (It.y > Hi.y) and (It.y < H0.y)):
                    #print("***Fingers Down***")

                    if (Tt.x > Hi.x):
                        #print("Hand Closed")
                        if ((Tt.x > Hi.x) and (Tt.x < Mt.x)):
                            if (Tt.y > In.y):
                                Read = "S"
                            elif (Tt.y < In.y):
                                Read = "T"
                        elif ((Tt.x > Mt.x) and (Tt.x < Pt.x)):
                            if (Tt.y > In.y):
                                Read = "N"
                            elif (Tt.y < In.y):
                                    Read = "M"
                    elif (Tt.y > Rt.y):
                        Read = "E"
                    elif (Tt.x < Hi.x):
                        Read = "A"

                elif((It.y > In.y) and (Tt.y > In.y) and (It.y > H0.y) and (Pt.y < In.y) and (Mt.y < In.y)):
                    Read = "Q"
                    
                elif((Pt.y > In.y) and (Rt.y > In.y) and (Mt.y > In.y) \
                    and (It.y > In.y) and (It.y < H0.y)):
                    if (comp*TRdist > 0.9):
                        Read = "C"
                    else:
                        Read = "O"
                    
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
                    if (Read == "-"): #Change This
                        NewRead = 0
                    else:
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
                    print("String: {}".format(String))
                      
                
            
    # Display the image
    cv2.imshow("Hand Landmarks with Numbers", image)
    
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        print("Word: {}".format(String))
        break

    

cap.release()
cv2.destroyAllWindows()


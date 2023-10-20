import cv2
import mediapipe as mp
import math
from statistics import mode

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
MYHAND = .2 #set scale of tested hand
DEBUG = False

# Euclidean distance
def compute_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)**0.5

hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    lis = []
    while (len(lis) < 40):
        #get video
        print()
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

                #get markers for each point
                Tt = hand_landmarks.landmark[4] #thumb tip
                Pt = hand_landmarks.landmark[20] #pinky tip
                H0 = hand_landmarks.landmark[0] #Hand 0 (wrist)
                Mt = hand_landmarks.landmark[12] #middle tip
                Hi = hand_landmarks.landmark[5] #index start
                Hp = hand_landmarks.landmark[17] #pinky start
                
                z_dist = -10000000*H0.z #set z distance constant
                
                z_scale = round(11/z_dist,2)
                
                #set hand scale
                scale = round((round(compute_distance(H0, Hi)*(z_scale), 2)) * (round(compute_distance(Hp, Hi)*(z_scale), 2)),2)
                

                comp = (round(scale/MYHAND,1))
                
                PTdist = abs(round(compute_distance(Pt, Tt)*(z_scale), 2))
                HPdist = abs(round(compute_distance(H0, Pt)*(z_scale), 2))
                HTdist = abs(round(compute_distance(H0, Tt)*(z_scale), 2))
                HMdist = abs(round(compute_distance(H0, Mt)*(z_scale), 2))
                
                #print("PTdist: {} Upper: {} Lower: {}".format((PTdist), comp*(1.1), comp*(.7)))
                if (((PTdist) < comp*(1.1)) and ((PTdist) >comp*(.7))):
                    lis.append("y")
                #print("")

    
    most_common = mode(lis)
    how_often = lis.count(most_common)
    if (how_often > (len(lis)/2)):
        print(most_common)
    else:
        print("")


                
            
    # Display the image
    cv2.imshow("Hand Landmarks with Numbers", image)
    
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()

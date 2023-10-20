import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
MYHAND = .07 #set scale of tested hand
DEBUG = False
FIND = False
ID = True

# Euclidean distance
def compute_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)**0.5

hands = mp_hands.Hands()

cap = cv2.VideoCapture(1)

while cap.isOpened():
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
            
            
            if (ID):
                if ((comp*PTdist) > (.30) and (comp*HMdist < 0.3) and (comp*HPdist > 0.3) and \
                    (comp*HRdist < 0.4) and (comp*HIdist < 0.4) and (comp*TtPs_dist > 0.2)):
                    print("Y")
                    
                elif((comp*HRdist < 0.75) and (comp*HIdist < 0.9) and (comp*HMdist < 0.75) \
                    and (HPdist < 0.75)):
                    #print("***Fingers Down***")

                    if (comp*TtPs_dist < 0.5):
                        #print("Hand Closed")
        
                        if (comp*HTdist < 0.64) and (comp*HTdist > 0.18):
                            print("E")
                        elif (comp*HTdist < 1.35) and (comp*HTdist > 0.64):
                            print("S")
                    

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
                print("PT:{}, HM:{}, HR:{}, HI:{}".format(PTdist, HMdist, HRdist, HIdist))  #for 'y'
                print("HTdist:{}, HTs_dist:{}, TIdist:{}".format(HTdist, HTs_dist, TIdist))
                print("HR: {}, HI: {}, HM: {}, HP: {}, TtPs: {}".format(HRdist, HIdist, HMdist, HPdist, TtPs_dist))
                print("")
                pass
                
            
                
            
    # Display the image
    cv2.imshow("Hand Landmarks with Numbers", image)
    
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()

'''
(comp*HTs_dist < 0.85) and (comp*HTs_dist > 0.55) and \
                     (comp*TIdist < 0.42) and (comp*TIdist > 0.15) and
                     '''

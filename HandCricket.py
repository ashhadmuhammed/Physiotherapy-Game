import cv2
import numpy as np
import time
import random
from tensorflow.keras.models import load_model
model = load_model(r'my_model_cc.h5')
cap = cv2.VideoCapture(0)
np.set_printoptions(formatter={'float_kind':'{:f}'.format})


user_move_name="***"

NUM_TO_VALUE = {
    0: "Defense",
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "None"
}

def mapper(val):
    return NUM_TO_VALUE[val]

start=(input("start?? y/n:"))
fps = 1
user_moves = []
pred_moves = []
pred_values = []
balls={"you":0,"sys":0}
runs={"you":0,"sys":0}
move_code=-1
score=0
out={"you":0,"sys":0}
toss=0
bat=""


while True:  
            return_value,frame = cap.read()
            fps+=1
            frame = cv2.flip(frame,1)

            if not return_value:
                continue

            cv2.rectangle(frame,(380,80),(604,304),(0,255,255),2)
            hand_img = frame[80:304,380:604]
 
            img = cv2.cvtColor(hand_img, cv2.COLOR_BGR2RGB)
            
            x=np.array([img],"float32")
            x/=255
            user_moves.append(x)
            
            img = cv2.imread("/home/mca/Desktop/ashhad/hand_cricket/HandCricketSimulation/black.jpg",cv2.IMREAD_COLOR)
            
            #predict after collecting 30 frames
            if fps==15 :
                
                for i in user_moves:
                    temp = np.array(i)
                    pred_moves.append(model.predict(temp))

                for i in pred_moves:
                    pred_values.append(np.argmax(i))
                
                move_code = max(set(pred_values), key = pred_values.count)
                
            
                # predict the move made
                computer_choices = ['zero', 'one', 'two', 'three', 'four', 'five', 'six']
                user_move_name = mapper(move_code)
            
                computer_move_name = random.choice(['zero', 'one', 'two', 'three', 'four', 'five', 'six'])               
                fps = 0
                user_moves = []
                pred_moves = []
                pred_values = [] 
            
            if start=='y':

                 if toss==0:
                    cv2.putText(img,"Toss",(100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(img,"six ::head",(100,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(img,"zero ::tail",(300,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    coin=random.choice([0,6])
                                        
                    if int(move_code)==coin:                      
                        toss=11
                        
                    elif (int(move_code)==0 or int(move_code)==6):
                          toss=1
                
                 elif toss==1 or toss==11:
                    if toss==11 and out["you"]==0:
                        
                        cv2.putText(img,"you won the toss and chose to bat",(150,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        # cv2.putText(img,"System won by 2 Runs",(150,125), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        # #user batting
                        bat="you"
                    
                        if (random.randint(0,6)==int(move_code) and fps==0):
                            out["you"]=1
                            bat="sys"
                            print("out")
              

                        elif(out[bat]==0 and balls[bat]<6 and fps==0):
                            balls[bat]+=1
                            runs[bat]+=int(move_code)
                            print(balls[bat])
                            print(runs[bat])
         
            if bat=="you":
                cv2.putText(img,"your are Batting",(150,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            elif bat=="sys":
                cv2.putText(img,"System is Batting",(150,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
            cv2.putText(img,"your score "+str(runs["you"])+" runs in "+str(balls["you"]),(150,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            cv2.putText(img,"system score "+str(runs["sys"])+" runs in "+str(balls["sys"]),(150,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "your move::"+user_move_name,(5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('score board',img)
            cv2.imshow("Hand Cricket", frame)
            # print(balls["you"],runs["you"])
            k = cv2.waitKey(10)
            if k == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
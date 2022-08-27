import mediapipe as mp
import cv2
from esp32tst import cam
import paho.mqtt.client as mqtt
import time
cap=cv2.VideoCapture(0)
mp_pose=mp.solutions.pose
mpDraw=mp.solutions.drawing_utils
pose=mp_pose.Pose()
p=[14:12:13]
def forward():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("forward",'utf-8')))
def turn():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("turn",'utf-8')))
def turn1():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("turn1",'utf-8')))
def stop():
    mqttBroker ="192.168.0.103"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("stop",'utf-8')))    

    


while True:
           success,frame=cap.read()
           if success==False:
               break
#           frame=cam() 
           frame=cv2.resize(frame,(640,480))
           rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
           result=pose.process(rgb_frame)
          
           mpDraw.draw_landmarks(frame,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
           list=[]
           if not result.pose_landmarks:
               print("nothing")
           else: 
               for id,lm in enumerate (result.pose_landmarks.landmark):
                    x=int(lm.x*640)
                    y=int(lm.y*480)
                    cv2.circle(frame,(x,y),1,(255,0,255),-1)
#                    cv2.putText(frame,str(id),(x,y -1),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
                    list.append([x,y])
        
               x1=(list[14][0])
               y1=(list[14][1])
               x2=(list[16][0])
               y2=(list[16][1])
               cv2.circle(frame,(x1,y1),4,(0,255,0),-1)
               cv2.circle(frame,(x2,y2),4,(0,255,0),-1)
               a=int(x1)//62
               cv2.putText(frame,str(a),(430,50),5,cv2.FONT_HERSHEY_PLAIN,(0,255,0),2)
               b=int(y2)//10
               
                        
               cv2.putText(frame,str(b),(30,50),5,cv2.FONT_HERSHEY_PLAIN,(255,0,0),2)
               if b > 42:
                 forward()
               else:
                    stop()
               if a < 4:
                 time.sleep(0.1)
                 turn1()
                 time.sleep(0.1)
                 stop()
               if a > 6:
                 time.sleep(0.1)
                 turn()
                 time.sleep(0.1)
                 stop()
#           count = p.count("31")
      
#           print('Count of 1:', count)             
           cv2.imshow("Frame", frame);
           key = cv2.waitKey(1) & 0xFF
           if key == ord("q"):
               break
cap.release()
cv2.destroyAllWindows()


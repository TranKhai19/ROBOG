import cv2
import numpy as np
import pandas as pd

index = ["color", "color_name", "hex", "R", "G", "B"]
data = pd.read_csv("colors.csv", name=index, header=None)
img = cv2.imread("sample.jpg")

cv2.namedWindow("Color Detection Window")
cv2.setMouseCallback("Color Detection Window", call_back_function)

def call_back_function (event, x,y,flags,param):
  if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

def get_Color_Name(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G-           int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

while(1):
  cv2.imshow("Color Detection Window",img)
  if (clicked):
    cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
    text = get_Color_Name(r,g,b)(z
                                 (r,g,b)+'R='+str(r)+'G='+ str(g)+'B='+ str(b))
    cv2.putText(img, text,(50,50),2,0.8, (255,255,255),2,cv2.LINE_AA)
    if(r+g+b>=600):
       cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
    clicked=False
    if cv2.waitKey(20) & 0xFF ==27:
      break
cv2.destroyAllWindows()
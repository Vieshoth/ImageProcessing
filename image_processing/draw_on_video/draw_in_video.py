import cv2
import numpy as np
  
       
pt1 = (0,0)
pt2 = (0,0)
leftButton_clicked = False
mouse_pressed = False
FIRST = True


def write_on(event, x, y, flags, param):
    # get mouse click
    global pt1, pt2, leftButton_clicked, mouse_pressed
    
    if event == cv2.EVENT_LBUTTONDOWN:
        leftButton_clicked = True
        pt1 = (x,y)
        
    if event == cv2.EVENT_MOUSEMOVE: 
        mouse_pressed = True
        pt2 = (x,y)
                   
    elif event == cv2.EVENT_LBUTTONUP: 
        leftButton_clicked = mouse_pressed = False

green = np.uint8([[[0,255,0 ]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)        
        

cap = cv2.VideoCapture(0)

cv2.namedWindow('drayimage')
cv2.setMouseCallback('drayimage', write_on)

while True:
    ret, frame = cap.read()

    if leftButton_clicked:
        cv2.circle(frame, center=pt1, radius=5, color=(0,255,0), thickness=-1)
        
    if leftButton_clicked and mouse_pressed:
        cv2.circle(frame, pt2, 10, color=(0,255,0), thickness=-1)
        
#masking is required here
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    
    hsv_lower =  np.array([59, 120, 120])
    hsv_higher  =  np.array([61,255,255])
    
    
    mask = cv2.inRange(frame_hsv, hsv_lower, hsv_higher)
    
    if FIRST :
        old_mask = mask
        FIRST = False
        
    mask = cv2.add(old_mask, mask)
    mask_inv = cv2.bitwise_not(mask)
    cont_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)

    cv2.imshow('frame',frame)
    
    cv2.imshow('mask',mask)
    
    
    cv2.imshow('drayimage',cont_frame)
    old_mask = mask
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
import datetime
import time

bgsMOG = cv2.createBackgroundSubtractorMOG2()
cap    = cv2.VideoCapture('video.avi')
counter = 0

if cap:
    while True:
        ret, frame = cap.read()

        if ret:            
            fgmask = bgsMOG.apply(frame, None, 0.1)
            cv2.line(frame,(70,0),(70,255),(255,255,0),1)
            # To find the countours of the Cars
            _,contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            try:
                hierarchy = hierarchy[0]

            except:
                hierarchy = []

            for contour, hier in zip(contours, hierarchy):
                (x, y, w, h) = cv2.boundingRect(contour)

                if w > 20 and h > 20:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 0)

                    #To find centroid of the Car
                    x1 = w/2      
                    y1 = h/2

                    cx = x+x1
                    cy = y+y1
                    print "cy=", cy
                    print "cx=", cx
                    centroid = (cx,cy)
                    print "centoid=", centroid
                    # Draw the circle of Centroid
                    cv2.circle(frame,(int(cx),int(cy)),2,(0,0,255),-1)

                    # To make sure the Car crosses the line
                    dy = cy-108
                    print "dy", dy
                    if centroid > (27, 38) and centroid < (134, 108):
                        if (cx >= 120):
                            counter +=1
                            print "counter=", counter
                        cv2.putText(frame, str(counter), (x,y-5),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (255, 0, 255), 2)
                        

            # draw the text and timestamp on the frame
            text = "Lancar"
            if counter >= 3:
                print "Macet", counter
                text = "MACET!!!"
            
            cv2.putText(frame, "Traffic Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            

            cv2.imshow('Output', frame)
            cv2.imshow('FGMASK', fgmask)
            key = cv2.waitKey(60)
            if key == 27:
                break

cap.release()
cv2.destroyAllWindows()

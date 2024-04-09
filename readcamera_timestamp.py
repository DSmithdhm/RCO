import cv2
import time
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
ret, frame = cap.read()
# Add timestamp. If frame invalid, ret == False & timestamp = 0
if ret == True:
    timestamp = int(time.time()*1000) # this is used in readradar.py & fusion.py
else:
    timestamp = 0
cv2.imwrite('image.jpg', frame)
cap.release()

import cv2
from picamera2 import Picamera2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  
# define a video capture object
#vid = cv2.VideoCapture(0)
picam2 = Picamera2()
picam2.start()

while(True):
      
    # Capture the video frame by frame
    #ret, frame = vid.read()
    frame = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5)
  
    # Display the resulting frame    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame_bgr, (x, y), (x+w, y+h), (0, 255, 0), 3)
    cv2.imshow('frame', frame_bgr)
    if cv2.waitKey(1) == ord('q'):
        break
  
# After the loop release the cap object
#vid.release()

# Destroy all the windows
cv2.destroyAllWindows()
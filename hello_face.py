#!/usr/bin/env python3

# Import required packages
from time import sleep, strftime
from datetime import datetime
import cv2
from picamera2 import Picamera2
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
 
def get_time_now():
    '''
    Get system time
    '''
    return datetime.now().strftime('%H:%M:%S')

def lcd_init():
    '''
    Initialize LCD object
    '''
    ## Intialize the LCD object using the PCF8574A MCP GPIO adapter
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    mcp = PCF8574_GPIO(PCF8574A_address)
    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    return lcd
    
def find_faces(lcd, message='Hello Face'):
    '''
    Loop over camera frames and search for faces. 
    If face detected display message on lcd
    '''
    print ('Detecting faces ... ')
    ## Initialize the picamera object
    picam = Picamera2()
    picam.start()

    ## Initializa frontal face clasifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while(True):
        # Capture frame            
        frame = picam.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame_bgr, (x, y), (x+w, y+h), (0, 255, 0), 3)
        
        # Display message
        if len(faces):
            lcd.clear()
            lcd.setCursor(0,0)  # set cursor position
            lcd.message(f'{message}\n')# display message
            lcd.message(get_time_now())   # display the time

        # Show frame
        cv2.imshow('frame', frame_bgr)
        if cv2.waitKey(1) == ord('q'):
            lcd.clear()
            break            
    
if __name__ == '__main__':
    lcd = lcd_init()
    try:
        find_faces(lcd)
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        lcd.clear()
        cv2.destroyAllWindows()


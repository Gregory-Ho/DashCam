# DashCam.py
# Gregory Ho
# Aug 2017
# Code for running a dash camera using a raspberry pi zero w
# Recording with 720p resolution, files are saved to local SD card

from datetime import datetime
from gpiozero import Button
from picamera import PiCamera
import time

def timeStamp(time, count):     # Generated a timestamp given a datetime object
    return str(time.year) + "-" + str(time.month) + "-" + str(time.day) + "-" + str(
        time.hour) + ":" + str(time.minute) + "(" + str(count) + ")"

partNumber = 0     # Keeps track of number of parts for the current recording session

carStatus = Button(21)      # Tells me if the car is on or off using GPIO21

camera = PiCamera()         # Declare a camera object and set the recording resolution
camera.resolution = (1280,720)

while True:     # Continuous loop for recording based on whether or not the car is on
    if carStatus.is_pressed:
        if partNumber == 0:             # Get the system time when the car is started (a session)
            sessionStartTime = datetime.now()
        partNumber += 1         # Increment the partNumber every time we start a new recording for the session
        newRecordingTime = datetime.now()
        camera.start_recording(timeStamp(newRecordingTime, partNumber) + ".h264")
        # print ("Started Recording")
        count = 0
        while carStatus.is_pressed and count <= 30: # Record 5 minute clips while car is on
            count += 1
            camera.wait_recording(10)       # Check car status every 10 seconds
            # print ("Checking Car Status")
        camera.stop_recording()
        # print ("Recording Stopped")
    else:   # Car has turned off
        partNumber = 0
        time.sleep(5)    # Burn some time
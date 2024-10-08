'''
 # @ Author: J.N. Hayek
 # @ Create Time: 2022-01-29 10:31:20
 # @ Description: Python script to detect and track particles from a given input.
 Applied to track and detect particles from J.D. Coral's microfluidic setup and recording.
 Uses the CV2 library to deal with the video capturing, video output, and user input. 
 Uses Trackpy as means of particle detection and tracking using a prescribed velocity model due to the distance of particles between frames.
'''
from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

# importing cv2 
import cv2 

from datetime import datetime

import numpy as np
import pandas as pd

import trackpy as tp
import trackpy.predict

################ Path setup
# Work path 
path = r'./'

cap = cv2.VideoCapture(path+"Input/mps_in_channel.mp4")
##########################################################################################
#Function Definition
##############################
# Filter model for detection
def detectFilter(imgFrame):
    fE= tp.locate(imgFrame, 11, invert=True, maxsize=5,minmass=200)

    f_interest= tp.locate(imgFrame, 11, invert=True, minmass=500)

    return fE, f_interest

# Prescribed linear velocity model
@trackpy.predict.predictor
def predict(t1, particle):
    velocity = np.array((150, 0))
    return particle.pos + velocity * (t1 - particle.t)
# Uncertainty window to search for tracked particle
SearchingArea = 100
##############################


# Variables
duration = 2
CTimes = 0
SavingDataBool = False
ListData = []
DataCollection = pd.DataFrame()
DataColInterest = pd.DataFrame()
NumFrame = 0

# Frames iteration loop
while True:
    success, img = cap.read()
    if not success:
        break
    img = img[10:-11,:]
    #Processing of the current frame to easen detection
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Register in the variable the pressed key
    k = cv2.waitKey(500) & 0xFF
    # press 'q' to exit
    if k == ord('q'):
        break
    # press 'c' to increase the CTimes counter and start a timer
    elif k == ord('c'):
        CTimes +=1 # Add 1 to CTimes per pressed c
        if not SavingDataBool:
            DataCollection = pd.DataFrame()
            DataColInterest = pd.DataFrame()
            ListData = []
            ListDataInterest = []
        SavingDataBool = True
        print("Pressed c: {} times".format(CTimes))  
        
        # start a timer
        start_time = datetime.now()

    # As CTimes = 0 is the state where nothing changes, checking for this will reduce the amount of operations per iteration 
    if CTimes!=0:
        # Calculate the difference in seconds between the timestamp and the current time
        diff = (datetime.now() - start_time).seconds
        # If the difference is under the prescribed duration, Print the consecutive number variable and add 1 to it to count for the current iteration 
        if (diff <= duration):
            # Detection step
            PD_particlesInFrame, PD_PartOfInterest = detectFilter(imgGray)
            # Fill the dataframe with the current frame number
            PD_particlesInFrame["frame"]=NumFrame
            PD_PartOfInterest["frame"]=NumFrame
            # Accumulate in a list all the dataframes to iterate throughout the tracking algorithm
            ListData.append(PD_particlesInFrame)
            ListDataInterest.append(PD_PartOfInterest)
            
            # Mark and label the detected particles
            [cv2.circle(img,(int(centroid[0]),int(centroid[1])), 10, (0, 0, 255), 1) for centroid in PD_particlesInFrame[["x","y"]].to_numpy()]
            [cv2.circle(img,(int(centroid[0]),int(centroid[1])), 10, (255, 0, 0), 1) for centroid in PD_PartOfInterest[["x","y"]].to_numpy()]

        else: # If the duration is larger than the set time, the CTimes counter resets
            # Velocity model used for the tracking
            DataCollection = pd.concat(tp.link_df_iter(ListData, SearchingArea, predictor=predict))
            DataColInterest = pd.concat(tp.link_df_iter(ListDataInterest, SearchingArea, predictor=predict))
            # Output filename
            StringDate = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Write the file onto a CSV
            DataCollection.to_csv(path + "Out/DetectedParticles_"+StringDate+".csv", sep=";")
            DataColInterest.to_csv(path + "Out/DetectedParticlesInterest_"+StringDate+".csv", sep=";")
            #Reset counters
            CTimes = 0
            SavingDataBool = False

    NumFrame +=1
    
    cv2.imshow("Video", img) 
#closing all open windows 
cv2.destroyAllWindows() 
'''
 # @ Author: J.N. Hayek
 # @ Create Time: 2022-01-27 08:44:46
 # @ Description: Python script to register an user's input.
'''
# importing cv2 
import cv2 
from datetime import datetime

################ Setup to make the code work on linux, ERASE TO USE IN YOUR IMPLEMENTATION
# path 
path = r'/home/nico/Documents/Extra/Programming/Random/Jesus-220126/Input/A.jpg'
  
# Reading an image in default mode
image = cv2.imread(path)
  
# Window name in which image is displayed
window_name = 'image'

# Using cv2.imshow() method 
# Displaying the image NEEDED TO MAKE THE LIBRARY CV2 WORK in linux
cv2.imshow(window_name, image)
##########################################################################################

# Variables
duration = 5
ToPrintConsecutiveNumbers = 0
CTimes = 0

while True:
    # Register in the variable 'k' a pressed key
    k = cv2.waitKey(100) & 0xFF
    # press 'q' to exit
    if k == ord('q'):
        break
    # press 'c' to increase the CTimes counter and start a timer
    elif k == ord('c'):
        CTimes +=1 # Add 1 to CTimes per pressed c
        print("Pressed c: {} times".format(CTimes))  

        # start a timer
        start_time = datetime.now()


    # As CTimes = 0 is the state where nothing changes, checking for this will reduce the amount of operations per iteration 
    if CTimes!=0:
        # Calculate the difference in seconds between the timestamp and the current time
        diff = (datetime.now() - start_time).seconds
        # If the difference is under the prescribed duration, Print the consecutive number variable and add 1 to it to count for the current iteration 
        if (diff <= duration):
            ToPrintConsecutiveNumbers += 1
            print ("My Consecutive number is {}".format(ToPrintConsecutiveNumbers))

        else: # If the duration is larger than the set time, the CTimes counter resets
            CTimes = 0

  
#closing all open windows 
cv2.destroyAllWindows() 
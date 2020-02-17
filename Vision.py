import cv2 as cv
import VisionEG as veg
from networktables import NetworkTables
import os

#NetworkTables initialization
NetworkTables.initialize(server='10.71.12.2')
table = NetworkTables.getTable('SmartDashboard')

def set_default():
    table.putNumber("Distance", -1)
    table.putNumber("Angle", 360)
    table.putBoolean("SeePowerPort", False)

#Camera
camera = veg.USBCamera(0, veg.Cameras.LIFECAM_3000.focal_length,
                   veg.Cameras.LIFECAM_3000.fov)
camera.set_width(640)
camera.set_height(480)

#Video Loop
while True:
    #Check if "StopVision" is True, if yes it shutdowns the Jetson
    if table.getBoolean("StopVision", False):
        os.system("sudo shutdown -h now")

    #Gets the frame and the coded frame from the camera, if the frame is none, CameraInput is set to False
    hsv_frame, frame = camera.get_colored_frame(cv.COLOR_BGR2HSV)
    if frame is None:
        table.putBoolean("CameraInput", False)
        continue
    table.putBoolean("CameraInput", True)

    #Treshholds the frame and cleans it with median_blur function
    tresh = cv.inRange(hsv_frame, veg.HSV_ranges.MacbookPro.Powercell.low,
                       veg.HSV_ranges.MacbookPro.Powercell.high)
    tresh = veg.median_blur(tresh, 7)

    #Finds the contours in the image
    contours = veg.find_contours(tresh)

    if len(contours) > 0:
        #Filter the contours, checks if the distance from the contour is between 2 and 7 if yes, it returns the biggest contour, else returns None
        contour = veg.get_biggest_filtered(
            contours, veg.Reflector.function_parameters, 2, 7)
        if contour is None:
            set_default()
            continue

        #Initializes a shape object and calculates the distance and the angle
        shape = veg.Shape(contour)
        distance = shape.calculate_distance_with_function(veg.Reflector.function_parameters)
        angle = shape.calculate_angle(veg.Cameras.LIFECAM_3000)

        #Puts the values at the networktable
        table.putBoolean("SeePowerPort", True)
        table.putNumber("Distance", distance)
        table.putNumber("Angle", angle)

    else:
        set_default()
    
    

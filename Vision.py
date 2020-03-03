import cv2 as cv
import VisionEG as veg
from networktables import NetworkTables
import os

# NetworkTables initialization
NetworkTables.initialize(server='10.71.12.2')
table = NetworkTables.getTable('SmartDashboard')

#window = veg.FeedWindow("window")
#window.open()

low_hsv_range = (table.getNumber("lowh", veg.HSV_ranges.LIFECAM_3000.Reflector.lowH),
                 table.getNumber("lows", veg.HSV_ranges.LIFECAM_3000.Reflector.lowS),
                 table.getNumber("lowv", veg.HSV_ranges.LIFECAM_3000.Reflector.lowV))
high_hsv_range = (table.getNumber("highh", veg.HSV_ranges.LIFECAM_3000.Reflector.highH),
                  table.getNumber("highs", veg.HSV_ranges.LIFECAM_3000.Reflector.highS),
                  table.getNumber("highv", veg.HSV_ranges.LIFECAM_3000.Reflector.highV))


def set_default():
    table.putNumber("Distance", -1)
    table.putNumber("Angle", 360)
    table.putBoolean("SeePowerPort", False) 


# Camera
camera = veg.USBCamera(0, veg.Cameras.LIFECAM_3000.focal_length,
                       veg.Cameras.LIFECAM_3000.fov)
window = veg.CameraWindow("Vision", camera)
window.open()
camera.set_width(640)
camera.set_height(480)                                           

counter = 0

# Video Loop
while True:

    # Check if "StopVision" is True, if yes it shutdowns the Jetson
    if table.getBoolean("StopVision", False):
        os.system("sudo shutdown -h now")

    # Gets the frame and the coded frame from the camera, if the frame is none, CameraInput is set to False
    hsv_frame, frame = camera.get_colored_frame(cv.COLOR_BGR2HSV)
    #window.show_frame(frame)
    if frame is None:
        table.putBoolean("CameraInput", False)
        continue
    table.putBoolean("CameraInput", True)

    # Treshholds the frame and cleans it with median_blur function
    tresh = cv.inRange(hsv_frame, low_hsv_range, high_hsv_range)
    tresh = veg.median_blur(tresh, 7)

    # Save the frame if TakePhoto is True
    if table.getBoolean("TakePhoto", False):
        table.putBoolean("TakePhoto", False)
        counter += 1
        cv.imwrite("frame" + str(counter) + ".jpg", frame)
        cv.imwrite("tresh" + str(counter) + ".jpg", tresh)

    window.show_frame(tresh)

    # Finds the contours in the image
    contours = veg.find_contours(tresh)

    if len(contours) > 0:
        # Filter the contours, checks if the distance from the contour is between 2 and 7 if yes, it returns the
        # biggest contour, else returns None contour = veg.get_biggest_filtered( contours,
        # veg.Reflector.function_parameters, 2, 7)
        contour = veg.biggest_contour(contours)
        if contour is None:
            set_default()
            continue

        # Initializes a shape object and calculates the distance and the angle
        shape = veg.Shape(contour)
        distance = shape.calculate_distance(veg.Reflector.center_height, veg.Cameras.LIFECAM_3000.height,
                                            veg.Cameras.LIFECAM_3000.angle, veg.Cameras.LIFECAM_3000.vertical_fov,
                                            veg.Cameras.LIFECAM_3000.middle)
        distance = 1.132197 * distance - 0.308952
        angle = shape.calculate_angle(veg.Cameras.LIFECAM_3000)

        print("distance = " + str(distance) + "\nAngle = " + str(angle))

        # Puts the values at the networktable
        table.putBoolean("SeePowerPort", True)
        table.putNumber("Distance", distance)
        table.putNumber("Angle", angle)

    else:
        set_default()
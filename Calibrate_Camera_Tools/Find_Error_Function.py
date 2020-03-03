import sys
sys.path.append('..')
import cv2 as cv
import VisionEG as veg

camera = veg.USBCamera(0, veg.Cameras.LIFECAM_3000.focal_length,
                   veg.Cameras.LIFECAM_3000.fov)

camera.set_width(640)
camera.set_height(480)

shape_window = veg.FeedWindow("shape")
shape_window.open()

distance_with_areas = []

while True:
    hsv_frame, frame = camera.get_colored_frame(cv.COLOR_BGR2HSV)
    if frame is None:
        exit()
    tresh = cv.inRange(hsv_frame, veg.HSV_ranges.LIFECAM_3000.Reflector.low,
                    veg.HSV_ranges.LIFECAM_3000.Reflector.high)
    tresh = veg.median_blur(tresh, 7)
    shape_window.show_frame(tresh)
    contours = veg.find_contours(tresh)
    if len(contours) > 0:
        contour = max(contours, key=cv.contourArea)
        if contour is None:
            continue
        shape = veg.Shape(contour)

        my_distance = shape.calculate_distance(veg.Reflector.center_height, veg.Cameras.LIFECAM_3000.height,
                                            veg.Cameras.LIFECAM_3000.angle, veg.Cameras.LIFECAM_3000.vertical_fov,
                                            veg.Cameras.LIFECAM_3000.middle)

        if shape_window.last_key_pressed == 'r':
            try:
                distance = float(input("Enter the distance from the object (in meters) >>> "))
            except:
                print("Invalid distance")
            if distance == 999:
                continue
            if distance == 1000:
                print(distance_with_areas)
            else:
                distance_with_areas.append((my_distance, distance))
            
        

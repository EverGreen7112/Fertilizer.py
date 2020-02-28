import sys
sys.path.append('..')
import cv2 as cv
import VisionEG as veg

camera = veg.USBCamera(0, veg.Cameras.LIFECAM_3000.focal_length,
                   veg.Cameras.LIFECAM_3000.fov)

camera.set_width(640)
camera.set_height(480)

cam_window = veg.CameraWindow("cam", camera)
shape_window = veg.FeedWindow("shape")
shape_window.open()
cam_window.open()

distance_with_areas = []

while True:
    hsv_frame, frame = cam_window.show_and_get_color_frame(cv.COLOR_BGR2HSV)
    if frame is None:
        exit()
    tresh = cv.inRange(hsv_frame, veg.HSV_ranges.LIFECAM_3000.ReflectorTest.low,
                    veg.HSV_ranges.LIFECAM_3000.ReflectorTest.high)
    tresh = veg.median_blur(tresh, 7)
    shape_window.show_frame(tresh)
    contours = veg.find_contours(tresh)
    if len(contours) > 0:
        contour = max(contours, key=cv.contourArea)
        if contour is None:
            continue
        shape = veg.Shape(contour)
        rect = veg.Rectangle(contour)
        #shape_window.show_frame(shape.draw(frame))
        
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
                distance_with_areas.append((shape.area, rect.area, distance))
            
        

from USBCamera import *
import cv2 as cv
from window import *
from constants import *
from cleaning_tools import *
from draw_on_frame import *
from find_tools import *
from shapes import *

camera = USBCamera(0, Cameras.LIFECAM_3000.focal_length,
                   Cameras.LIFECAM_3000.fov)
cam_window = CameraWindow("cam", camera)
tresh_window = FeedWindow("treshhold")
rect_window = FeedWindow("rect")
rect_window.open()
tresh_window.open()
cam_window.open()
rect_window.add_trackbar("focal_length", int(Cameras.LIFECAM_3000.focal_length), 1500, 
                         lambda *args: None)

while True:
    hsv_frame, frame = cam_window.show_and_get_color_frame(cv.COLOR_BGR2HSV)
    if frame is None:
        break
    tresh = cv.inRange(hsv_frame, HSV_ranges.LIFECAM_3000.Reflector.low,
                       HSV_ranges.LIFECAM_3000.Reflector.high)
    tresh = median_blur(tresh, 11)
    contours = find_contours(tresh)
    if len(contours) > 0:
        biggest_contour = max(contours, key=cv.contourArea)
        shape = Rectangle(biggest_contour)
        distance = shape.calculate_distance(
            0.6513, rect_window.get_trackbar_pos("focal_length"))
        angle = shape.calculate_angle(Cameras.LIFECAM_3000)
        print("Distance = " + str(distance) + "\n Angle = " + str(angle))
        frame_to_draw = shape.draw(frame)
        rect_window.show_frame(frame_to_draw)
    tresh_window.show_frame(tresh)

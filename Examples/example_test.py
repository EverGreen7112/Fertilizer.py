from USBCamera import *
import cv2 as cv
from window import *
from constants import *
from cleaning_tools import *
from draw_on_frame import *
from find_tools import *
from shapes import *

camera = USBCamera(0, Cameras.LIFECAM_3000.focal_length, Cameras.LIFECAM_3000.fov)
cam_window = CameraWindow("cam", camera)
tresh_window = FeedWindow("treshhold")
rect_window = FeedWindow("rect")
rect_window.open()
tresh_window.open()
cam_window.open()
while True:
    hsv_frame, frame = cam_window.show_and_get_color_frame(cv.COLOR_BGR2HSV)
    if frame is None:
        break
    tresh = cv.inRange(hsv_frame, HSV_ranges.LIFECAM_3000.Powercell.low, HSV_ranges.LIFECAM_3000.Powercell.high)
    tresh = median_blur(tresh, 11)
    contours = find_contours(tresh)
    if len(contours) > 0:
        biggest_contour = max(contours, key = cv.contourArea)
        shape = Rectangle(biggest_contour)
        frame_to_draw = shape.draw(frame)
        rect_window.show_frame(frame_to_draw)
    tresh_window.show_frame(tresh)

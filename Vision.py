import cv2 as cv
import VisionEG as veg

camera = veg.USBCamera(0, veg.Cameras.LIFECAM_3000.focal_length,
                   veg.Cameras.LIFECAM_3000.fov)
camera.set_width(640)
camera.set_height(480)
cam_window = veg.CameraWindow("cam", camera)
tresh_window = veg.FeedWindow("treshhold")
rect_window = veg.FeedWindow("rect")
rect_window.open()
tresh_window.open()
cam_window.open()
rect_window.add_trackbar("focal_length", int(veg.Cameras.LIFECAM_3000.focal_length), 1500,
                         lambda *args: None)

while True:
    hsv_frame, frame = cam_window.show_and_get_color_frame(cv.COLOR_BGR2HSV)
    if frame is None:
        break
    tresh = cv.inRange(hsv_frame, veg.HSV_ranges.LIFECAM_3000.Reflector.low,
                       veg.HSV_ranges.LIFECAM_3000.Reflector.high)
    tresh = veg.median_blur(tresh, 7)
    contours = veg.find_contours(tresh)
    if len(contours) > 0:
        biggest_contour = max(contours, key=cv.contourArea)
        tmp = veg.Shape_for_distance(biggest_contour, veg.Reflector.real_area, 697)
        print(str(tmp.area) + " " + str(tmp.distance))
        shape = veg.Shape(biggest_contour)
        distance = shape.calculate_distance(
            veg.Reflector.real_area, rect_window.get_trackbar_pos("focal_length"))
        angle = shape.calculate_angle(veg.Cameras.LIFECAM_3000)
        frame_to_draw = shape.draw(frame)
        rect_window.show_frame(frame_to_draw)
    tresh_window.show_frame(tresh)

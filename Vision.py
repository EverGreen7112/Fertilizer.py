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
        exit()
    tresh = cv.inRange(hsv_frame, veg.HSV_ranges.LIFECAM_3000.Reflector.low,
                       veg.HSV_ranges.LIFECAM_3000.Reflector.high)
    tresh = veg.median_blur(tresh, 7)
    contours = veg.find_contours(tresh)
    if len(contours) > 0:
        contour = veg.get_biggest_filtered(
            contours, veg.Reflector.real_area,rect_window.get_trackbar_pos("focal_length"), 2, 7)
        if contour is None:
            continue
        shape = veg.Shape(contour)
        #distance = shape.calculate_distance(
         #   veg.Reflector.real_area, rect_window.get_trackbar_pos("focal_length"))
        x = shape.area
        distance = 1.843515 + 0.01090572*x - 0.0000116416*x**2 + 0.000000004938927*x**3 -0.00000000000096809253*x**4 + 0.00000000000000007239259*x**5
        angle = shape.calculate_angle(veg.Cameras.LIFECAM_3000)
        print("distance = " + str(distance) + " angle = " + str(angle))
        frame_to_draw = shape.draw(frame)
        rect_window.show_frame(frame_to_draw)
    tresh_window.show_frame(tresh)

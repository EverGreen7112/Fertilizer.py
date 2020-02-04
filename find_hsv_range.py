from window import *
from USBCamera import USBCamera
import cv2 as cv
import numpy as np

my_range = np.array([40, 40, 40])

camera = USBCamera(0, 100, 100)
camera.set_exposure(-100)
window = CameraWindow("Find_HSV_ranges", camera)
window.open()

def crop(frame, x, y, w, h):
    return frame[y:y + h, x:x + w]

med = None
while True:
    HSV_frame, frame = window.show_and_get_color_frame(cv.COLOR_BGR2HSV)
    if frame is None:
        break
    if window.last_key_pressed == 'r':
        box = cv.selectROI('Find_HSV_ranges', frame)
        cropped_frame = crop(HSV_frame, *box)
        med = np.median(cropped_frame, axis=(0, 1)).astype(int)
        if type(med) is not np.ndarray:
            med = np.array([med])
        break

ranges = np.array([med - my_range, med + my_range])
for tmp_range in ranges:
    for i, num in enumerate(tmp_range):
        num = min(255, max(0, num))
        tmp_range[i] = num

print(ranges)
import sys
sys.path.append('..')
import VisionEG as veg
import numpy as np
import cv2 as cv

def crop(frame, x, y, w, h):
        """
        Crops the frame
        """
        return frame[y:y + h, x:x + w]


window = veg.FeedWindow("Find_HSV_ranges_from_image")
my_range = np.array([40, 40, 40])
path = input("Enter the file name >>> ")
frame = cv.imread(path)
hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
box = cv.selectROI("Find_HSV_ranges_from_image", frame)
cropped_frame = crop(hsv_frame, *box)
med = np.median(cropped_frame, axis=(0, 1)).astype(int)
if type(med) is not np.ndarray:
    med = np.array([med])

ranges = np.array([med - my_range, med + my_range])
for tmp_range in ranges:
    for i, num in enumerate(tmp_range):
        num = min(255, max(0, num))
        tmp_range[i] = num

print(ranges)

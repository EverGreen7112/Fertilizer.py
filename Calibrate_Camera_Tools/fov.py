import sys
sys.path.append('..')
import numpy as np
import cv2 as cv
import VisionEG as veg

def find_fov(bbox, dimension, z, camera_dimension):
    return [np.arctan(dimension[i] / z) * camera_dimension[i] / bbox[i + 2] for i in range(2)]


print('place object in the middle of the frame and press r')
width = float(input('Enter object width in meters >>> '))
height = float(input('Enter object height in meters >>> '))
z = float(input('Enter distance from object in the Z axis in meter units >>> '))
camera = veg.USBCamera(0, 100, 100)
camera.set_width(640)
camera.set_height(480)
window = veg.CameraWindow('Find_fov', camera)
window.open()
while True:
    frame = window.show_and_get_frame()
    k = window.last_key_pressed
    if k == 'r':
        bbox = cv.selectROI('Find_fov', frame)
        fov = find_fov(bbox, (width, height), z, (camera.get_width(), camera.get_height()))
        break
cv.destroyAllWindows()

print(f'width fov: {fov[0]} \nheight fov: {fov[1]}')





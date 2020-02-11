import cv2 as cv
from shapes import *


def distance_filter(contours, original_area, focal_length, min_distance, max_distance):
    passed_contours = []
    for contour in contours:
        tmp_distance_shape = Shape_for_distance(
            contour, original_area, focal_length)
        if(tmp_distance_shape.distance > min_distance and tmp_distance_shape.distance < max_distance):
            passed_contours.append(tmp_distance_shape)
    return passed_contours


def get_biggest_filtered(contours, original_area, focal_length, min_distance, max_distance):
    passed_contours = distance_filter(
        contours, original_area, focal_length, min_distance, max_distance)
    if len(passed_contours) == 0: return None
    biggest_passed = max(passed_contours, key=lambda x: x.area)
    return biggest_passed.contour

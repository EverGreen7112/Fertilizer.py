import VisionEG
import cv2 as cv


class Shape:
    def __init__(self, contour):
        self.contour = contour
        self.center = VisionEG.get_shape_center(contour)
        self.area = VisionEG.get_shape_area(contour)

    def calculate_distance(self, original_area: float, focal_length: float) -> float:
        distance_from_rect = VisionEG.find_distance_from_objecet(
            focal_length, self.area, original_area)
        return distance_from_rect

    def calculate_angle(self, camera) -> float:
        distance_from_center_of_image = VisionEG.distance_from_center(
            self.center, camera.middle)
        angle = VisionEG.find_angle(distance_from_center_of_image,
                           camera.fov, camera.image_total_pixels)
        return angle

    def draw(self, frame_to_draw_on, color=(0, 255, 0), thick=1):
        frame_to_draw_on = VisionEG.deepcopy(frame_to_draw_on)
        cv.drawContours(frame_to_draw_on, [self.contour], 0, color, thick)
        return frame_to_draw_on


class Circle(Shape):
    def __init__(self, contour):
        self.center, self.radius = VisionEG.get_circle_value(contour)
        self.area = VisionEG.get_circle_area(self.radius)

    def draw(self, frame_to_draw_on):
        return VisionEG.draw_circle(frame_to_draw_on, self.center, self.radius)


class Rectangle(Shape):
    def __init__(self, contour):
        self.point1, self.point2 = VisionEG.get_rectangle_value(contour)
        self.area = VisionEG.get_rect_area(self.point1, self.point2)
        self.center = VisionEG.middle_of_rect(self.point1, self.point2)

    def calculate_angle(self, camera) -> float:
        distance_from_center = VisionEG.distance_from_center__rect(
            self.point1, self.point2, camera.middle)
        angle = VisionEG.find_angle(distance_from_center, camera.fov,
                           camera.image_total_pixels)
        return angle

    def draw(self, frame_to_draw_on):
        return VisionEG.draw_rectangle(frame_to_draw_on, self.point1, self.point2)


class Shape_for_distance(Shape):
    def __init__(self, contour, original_area: float, focal_length: float):
        self.area = VisionEG.get_shape_area(contour)
        self.contour = contour
        self.distance = self.calculate_distance(
            original_area, focal_length)

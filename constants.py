class HSV_ranges:
    """
    HSV ranges of objects that we want to track
    """
    class LIFECAM_3000:

        class Reflector:
            lowH = 38
            lowS = 142
            lowV = 181

            highH = 118
            highS = 222
            highV = 255

            low = (lowH, lowS, lowV)
            high = (highH ,highS, highV)
        class Powercell:
            """
            Contains the HSV ranges of the powercell 
            """
            lowH = 0
            lowS = 147
            lowV = 169

            highH = 66
            highS = 231
            highV = 255

            low = (lowH, lowS, lowV)
            high = (highH, highS, highV)
        
    class MacbookPro:

        class Reflector:
            lowH = 38
            lowS = 142
            lowV = 181

            highH = 118
            highS = 222
            highV = 255

            low = (lowH, lowS, lowV)
            high = (highH ,highS, highV)

        class Powercell:
            """
            Contains the HSV ranges of the powercell 
            """
            lowH = 22
            lowS = 115
            lowV = 80

            highH = 38
            highS = 242
            highV = 255

            low = (lowH, lowS, lowV)
            high = (highH, highS, highV)


class Powercell:
    """
    Information about the powercell
    """
    area = 0.099 #In meters

class Reflector:
     """
    Information about the life reflectors
    """

class Cameras:
    """
    Information about cameras
    TODO add the front camera
    """
    class LIFECAM_3000:
        """
        Information about our back camera who tracks the reflective tapes
        """
        focal_length = 697.0395744431028
        fov = 53
        middle = (640, 360)
        image_total_pixels = middle[0] * 2
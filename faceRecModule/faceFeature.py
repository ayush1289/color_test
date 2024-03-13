import cv2
import numpy as np
import dlib

class FaceFeatures:
    """
    Class to extract facial features and their colors from an image.
    """

    def __init__(self, filepath: str):
        """
        Initializes the FaceFeatures object with the given image filepath.
        
        Args:
            filepath (str): Path to the image file.
        """
        self.filepath = filepath
        self.img = cv2.imread(filepath)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.left_eye_colour = None
        self.right_eye_colour = None
        self.nose_colour = None
        self.jaw_colour = None
        self.lips_colour = None

    def __str__(self):
        """
        String representation of the FaceFeatures object.
        """
        return f"""
                left_eye_colour == {self.left_eye_colour},
                right_eye_colour == {self.right_eye_colour},
                nose_colour == {self.nose_colour},
                jaw_color == {self.jaw_colour},
                lips_color == {self.lips_colour}
            """

    def get_hexcode(self, img, pixel_val):
        """
        Convert BGR pixel values to hexadecimal color code.
        
        Args:
            img (numpy.ndarray): Image array.
            pixel_val (tuple): Tuple containing (x, y) pixel coordinates.

        Returns:
            str: Hexadecimal color code.
        """
        x, y = pixel_val
        b, g, r = img[y, x]

        hexcode = "#{:02x}{:02x}{:02x}".format(r, g, b)
        return hexcode

    def find_face_features(self):
        """
        Detect facial landmarks using dlib library.
        
        Returns:
            numpy.ndarray: Array of detected facial landmarks.
        """
        imgGray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.detector(imgGray, 0)
        for face in faces:
            x1, y1 = face.left(), face.top()
            x2, y2 = face.right(), face.bottom()

            landmarks = self.predictor(imgGray, face)

            points = []
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                points.append([x, y])
            points = np.array(points)
        return points

    def get_features_colour(self, points):
        """
        Extract the major color from specific facial feature regions.
        
        Args:
            points (numpy.ndarray): Array of detected facial landmarks.

        Returns:
            tuple: Hexadecimal color codes of facial features.
        """
        imgLeftEye_x = (points[36][0] + points[42][0]) // 2
        imgLeftEye_y = (points[36][1] + points[42][1]) // 2

        imgRightEye_x = (points[45][0] + points[39][0]) // 2
        imgRightEye_y = (points[45][1] + points[39][1]) // 2

        imgLips_x = (points[48][0] + points[54][0]) // 2
        imgLips_y = (points[48][1] + points[54][1]) // 2

        imgNose_x = (points[31][0] + points[35][0]) // 2
        imgNose_y = (points[31][1] + points[35][1]) // 2

        imgJaw_x = (points[0][0] + points[16][0]) // 2
        imgJaw_y = (points[0][1] + points[16][1]) // 2

        self.left_eye_colour = self.get_hexcode(self.img, (imgLeftEye_x, imgLeftEye_y))
        self.right_eye_colour = self.get_hexcode(self.img, (imgRightEye_x, imgRightEye_y))
        self.nose_colour = self.get_hexcode(self.img, (imgNose_x, imgNose_y))
        self.jaw_colour = self.get_hexcode(self.img, (imgJaw_x, imgJaw_y))
        self.lips_colour = self.get_hexcode(self.img, (imgLips_x, imgLips_y))
        return (
            self.left_eye_colour,
            self.right_eye_colour,
            self.nose_colour,
            self.jaw_colour,
            self.lips_colour,
        )

if __name__ == "__main__":

    obj = FaceFeatures("img.jpg")
    points = obj.find_face_features()
    obj.get_features_colour(points)
    print(obj)

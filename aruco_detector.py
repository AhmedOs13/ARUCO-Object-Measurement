# aruco_detector.py
import cv2
import numpy as np



class ArucoDetector:
    def __init__(self, frame_dimensions, settings):
        self.MARKER_LENGTH_CM = settings[0]
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)

        # Initialize camera matrix
        frame_width, frame_height = frame_dimensions
        focal_length = settings[1]
        self.camera_matrix = np.array([
            [focal_length, 0, frame_width],
            [0, focal_length, frame_height],
            [0, 0, 1]
        ])
        self.dist_coeffs = np.zeros((4, 1))

    def detect_markers(self, frame):
        corners, ids, rejected = self.detector.detectMarkers(frame)
        return corners, ids

    def get_marker_length(self):
        return self.MARKER_LENGTH_CM
# camera_handler.py
import cv2


class CameraHandler:
    def __init__(self, camera_mode):
        self.camera_mode = camera_mode
        self.cap = self._initialize_camera()

        if not self.cap.isOpened():
            raise Exception("Could not connect to the camera.")

        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def _initialize_camera(self):
        if self.camera_mode == '1':
            return cv2.VideoCapture(0)
        elif self.camera_mode == '2':
            IP_WEBCAM_URL = input('>> ENTER YOUR IP: ')
            return cv2.VideoCapture(IP_WEBCAM_URL)
        else:
            raise ValueError("Invalid camera mode selected.")

    def read_frame(self):
        return self.cap.read()

    def get_frame_dimensions(self):
        return self.frame_width, self.frame_height

    def release(self):
        self.cap.release()
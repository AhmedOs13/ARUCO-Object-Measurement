# measurement_processor.py
import cv2
import numpy as np


class MeasurementProcessor:
    def __init__(self, detector):
        self.detector = detector

    def process_frame(self, frame, corners, ids):
        if len(corners) > 0:
            ref_corners = corners[0][0]
            marker_length = self.detector.get_marker_length()

            marker_width = np.linalg.norm(ref_corners[0] - ref_corners[1])
            marker_height = np.linalg.norm(ref_corners[1] - ref_corners[2])
            pixel_cm_ratio_width = marker_length / marker_width
            pixel_cm_ratio_height = marker_length / marker_height

            self._process_objects(frame, pixel_cm_ratio_width, pixel_cm_ratio_height)

    def _process_objects(self, frame, pixel_cm_ratio_width, pixel_cm_ratio_height):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        frame_height, frame_width = frame.shape[:2]

        for cnt in contours:
            if cv2.contourArea(cnt) < 500:
                continue

            try:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                if len(box) >= 4:
                    box = np.int64(box)
                    (x, y), (width, height), angle = rect

                    object_width = width * pixel_cm_ratio_width
                    object_height = height * pixel_cm_ratio_height

                    if object_width > frame_width or object_height > frame_height:
                        continue

                    self._draw_measurements(frame, box, x, y, object_width, object_height)

            except Exception as e:
                print(f"Error processing contour: {e}")
                continue

    def _draw_measurements(self, frame, box, x, y, width, height):
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
        cv2.putText(frame, f"Width: {width:.2f} cm",
                    (int(x) - 100, int(y) - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, f"Height: {height:.2f} cm",
                    (int(x) - 100, int(y) + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
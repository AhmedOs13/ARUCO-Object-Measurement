# main.py
import cv2
import numpy as np
from camera_handler import CameraHandler
from aruco_detector import ArucoDetector
from measurement_processor import MeasurementProcessor
from menu_system import MenuSystem
from camera_calibration import calibrate


def main():
    menu = MenuSystem()

    while True:
        choice = menu.show_main_menu()

        if choice == '1':  # Start Measurement
            try:
                # Initialize camera
                settings = np.genfromtxt('settings.csv', delimiter=',', skip_header=1)
                camera_mode = menu.show_camera_menu()
                camera = CameraHandler(camera_mode)

                # Initialize detector and processor
                detector = ArucoDetector(camera.get_frame_dimensions(), settings)
                processor = MeasurementProcessor(detector)

                # Start measurement loop
                run_measurement_system(camera, detector, processor)

            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")

        elif choice == '2':  # Camera Calibration
            try:
                camera_mode = menu.show_camera_menu()
                camera = CameraHandler(camera_mode)
                camera_matrix, dist_coeffs, error = calibrate()
                if camera_matrix is not None:
                    print("\nCalibration parameters saved successfully!")
                    input("Press Enter to continue...")
                camera.release()
            except Exception as e:
                print(f"Calibration error: {e}")
                input("Press Enter to continue...")

        elif choice == '3':  # Settings
            menu.show_settings_menu()

        elif choice == '4':  # Exit
            print("Exiting program...")
            break


def run_measurement_system(camera, detector, processor):
    while True:
        ret, frame = camera.read_frame()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        corners, ids = detector.detect_markers(frame)
        if len(corners) > 0:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            processor.process_frame(frame, corners, ids)

        cv2.imshow('Object Measurement', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

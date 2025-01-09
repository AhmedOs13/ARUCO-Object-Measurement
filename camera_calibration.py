import cv2
import numpy as np
import glob
import os



class SquareCalibrator:
    def __init__(self, checkerboard_size=(7, 7), square_size=9.0, image_folder=None, save_folder=None):
        """
        Initialize the calibrator for camera calibration using a checkerboard.
        :param checkerboard_size: Number of inner corners per a chessboard row and column.
        :param square_size: The size of each square on the checkerboard (in cm).
        :param image_folder: Folder containing the calibration images.
        :param save_folder: Folder to save the calibration results.
        """
        self.checkerboard_size = checkerboard_size
        self.square_size = square_size
        self.image_folder = image_folder
        self.save_folder = save_folder

        # 3D points in real world space
        self.obj_points = []
        # 2D points in image plane
        self.img_points = []

        # Prepare a single object points template
        self.obj_point_template = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
        self.obj_point_template[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)
        self.obj_point_template *= square_size  # Scale by square size

    def detect_corners(self, image):
        """
        Detect checkerboard corners in the given image.
        :param image: Input image.
        :return: Detected corners if found, else None.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, self.checkerboard_size, None)

        if ret:
            # Refine corner locations for higher accuracy
            corners = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1),
                criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            )
            return corners
        return None

    def add_calibration_data(self, image):
        """
        Add calibration data from the image if checkerboard is detected.
        :param image: Input image for calibration.
        :return: True if successful, False otherwise.
        """
        corners = self.detect_corners(image)
        if corners is not None:
            self.obj_points.append(self.obj_point_template)
            self.img_points.append(corners)
            return True
        return False

    def calibrate_camera(self, image_size):
        """
        Perform camera calibration.
        :param image_size: Tuple (width, height) of the images.
        :return: Camera matrix, distortion coefficients, and calibration error.
        """
        if len(self.obj_points) == 0:
            raise ValueError("No calibration data available. Make sure to add images with detected corners.")

        ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
            self.obj_points, self.img_points, image_size, None, None
        )

        if not ret:
            raise ValueError("Calibration failed. Check the input images and points.")

        # Calculate the re-projection error
        mean_error = 0
        for i in range(len(self.obj_points)):
            img_points2, _ = cv2.projectPoints(self.obj_points[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs)
            error = cv2.norm(self.img_points[i], img_points2, cv2.NORM_L2) / len(img_points2)
            mean_error += error
        mean_error /= len(self.obj_points)

        return camera_matrix, dist_coeffs, mean_error

    def run_calibration(self):
        """
        Process all images in the specified folder and perform calibration.
        :return: Camera matrix, distortion coefficients, and calibration error.
        """
        if not self.image_folder or not self.save_folder:
            raise ValueError("Image folder and save folder must be provided.")

        images = glob.glob(os.path.join(self.image_folder, '*.jpg'))  # Adjust extension as needed

        print("=== Camera Calibration ===")
        print(f"Processing {len(images)} images from {self.image_folder}")

        for img_path in images:
            image = cv2.imread(img_path)
            if image is None:
                print(f"Could not load image: {img_path}")
                continue

            success = self.add_calibration_data(image)
            if success:
                print(f"Checkerboard detected in {img_path}")
            else:
                print(f"Checkerboard NOT detected in {img_path}")

        # Perform calibration
        if len(self.obj_points) > 0:
            sample_image = cv2.imread(images[0])
            height, width = sample_image.shape[:2]
            camera_matrix, dist_coeffs, error = self.calibrate_camera((width, height))

            # Save results
            if not os.path.exists(self.save_folder):
                os.makedirs(self.save_folder)

            np.save(os.path.join(self.save_folder, 'camera_matrix.npy'), camera_matrix)
            np.save(os.path.join(self.save_folder, 'dist_coeffs.npy'), dist_coeffs)

            print("\nCalibration successful!")
            print(f"Re-projection error: {error}")
            print("Camera matrix and distortion coefficients saved.")
            return camera_matrix, dist_coeffs, error
        else:
            print("No valid images for calibration. Calibration failed.")
            return None, None, None


def calibrate():
    image_folder = "checkerboard_images"
    save_folder = "results"

    calibrator = SquareCalibrator(
        checkerboard_size=(6, 8),
        square_size=2.5,
        image_folder=image_folder,
        save_folder=save_folder
    )

    return calibrator.run_calibration()

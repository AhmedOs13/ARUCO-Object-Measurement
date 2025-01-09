# ARUCO-Object-Measurement

A Python-based computer vision system that uses ArUco markers for real-time object measurement through camera feeds. The system can measure objects using either a default camera or an IP webcam, with support for camera calibration to ensure accurate measurements.

## Features

- Real-time object measurement using ArUco markers as reference
- Support for multiple camera inputs (default camera or IP webcam)
- Camera calibration using checkerboard pattern
- Interactive menu system for easy navigation
- Adjustable settings for marker length, focal length, and threshold values
- Visual feedback with measurement overlay on detected objects

## Prerequisites

- Python 3.x
- OpenCV (cv2)
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AhmedOs13/ARUCO-Object-Measurement.git
cd ARUCO-Object-Measurement
```

2. Install required dependencies:
```bash
pip install opencv-python numpy
```

## Project Structure

- `main.py` - Main application entry point
- `camera_handler.py` - Camera input management
- `aruco_detector.py` - ArUco marker detection
- `measurement_processor.py` - Object measurement processing
- `menu_system.py` - User interface and settings management
- `camera_calibration.py` - Camera calibration functionality

## Usage

1. Start the application:
```bash
python main.py
```

2. Main Menu Options:
   - **Start Measurement**: Begin real-time object measurement
   - **Camera Calibration**: Calibrate camera using checkerboard pattern
   - **Settings**: Adjust system parameters
   - **Exit**: Close the application

### Camera Calibration

1. Create a directory named `checkerboard_images` in the project root
2. Place checkerboard pattern images in the directory
3. Select "Camera Calibration" from the main menu
4. Follow the on-screen instructions
5. Calibration results will be saved in the `results` directory

### Measurement Process

1. Select "Start Measurement" from the main menu
2. Choose camera input (Default Camera or IP Webcam)
3. Place an ArUco marker (5x5, ID: 0-49) next to the object to measure
4. The system will display real-time measurements on screen
5. Press 'q' to exit measurement mode

## Settings

Adjust the following parameters through the Settings menu:
- Marker Length: Size of ArUco marker in centimeters
- Focal Length: Camera focal length for distance calculations
- Threshold Value: Binary threshold for object detection

## Error Handling

The system includes comprehensive error handling for:
- Camera connection failures
- Invalid camera modes
- Calibration errors
- Frame processing issues

## Development

### Key Components

1. **CameraHandler**: Manages camera input streams
2. **ArucoDetector**: Handles ArUco marker detection and processing
3. **MeasurementProcessor**: Processes frames and calculates measurements
4. **MenuSystem**: Provides user interface and settings management
5. **SquareCalibrator**: Handles camera calibration using checkerboard patterns

### Adding New Features

1. Create new component in a separate file
2. Import and integrate in `main.py`
3. Update menu system if needed
4. Add error handling
5. Test thoroughly

## Limitations

- Requires good lighting conditions for accurate measurements
- ArUco marker must be clearly visible in the frame
- Performance depends on camera quality and resolution
- Measurements are approximate and depend on proper calibration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

- OpenCV team for the computer vision library
- ArUco marker system developers

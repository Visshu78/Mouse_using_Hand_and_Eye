# Brightness Control Using Hand Gestures (OpenCV)

This project enables the control of the system's brightness using hand gestures. It leverages the power of **OpenCV** and **MediaPipe** for real-time hand and face mesh detection. The system tracks the position of the user's hand to adjust the brightness, providing an intuitive, hands-free method of controlling the screen's brightness.

## Key Features

- **Hand Gesture Detection**: Using **MediaPipe**, the hand gestures are tracked to adjust the brightness of the system.
- **Eye-Controlled Clicks**: The project also includes functionality to simulate mouse clicks based on eye closures, using **MediaPipe Face Mesh** to track eye movements.
- **Real-Time Interaction**: The system interacts in real-time with the user's movements, making it ideal for hands-free control.

## Tech Stack

- **Python**: The main programming language used.
- **OpenCV**: For image processing and capturing camera frames.
- **MediaPipe**: For hand tracking and facial landmark detection.
- **PyAutoGUI**: To simulate mouse actions such as movement and clicking.

## Installation

To run this project, ensure you have the following dependencies installed:

1. **Python** 3.x or higher
2. Install the necessary libraries:
   ```bash
   pip install opencv-python mediapipe pyautogui

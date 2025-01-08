import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize camera, hand detector, face mesh, and drawing utilities
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils

# Screen dimensions and camera frame ratios
screen_w, screen_h = pyautogui.size()
frame_w_ratio = screen_w / cam.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_h_ratio = screen_h / cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Variables to manage timing and state
previous_time = 0
eye_closed_time = 0
click_threshold = 0.25  # 0.7 seconds for eye closure to trigger click
double_click_threshold = 0.15  # Max interval for double click
click_times = []  # List to store click timestamps
is_clicking = False  # State to track if clicking is in progress

while True:
    success, frame = cam.read()
    if not success:
        break

    # Flip the frame and convert to RGB for processing
    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    current_time = time.time()

    # Process hand detection
    hand_output = hand_detector.process(rgb_frame)
    hands = hand_output.multi_hand_landmarks

    # Process face mesh for eye-controlled clicking
    face_output = face_mesh.process(rgb_frame)
    landmarks_points = face_output.multi_face_landmarks

    # Hand tracking for mouse movement
    if hands:
        for hand in hands:
            index_finger = hand.landmark[8]
            index_x, index_y = int(index_finger.x * frame_w), int(index_finger.y * frame_h)
            screen_index_x, screen_index_y = index_x * frame_w_ratio, index_y * frame_h_ratio
            pyautogui.moveTo(screen_index_x, screen_index_y, duration=0)
            cv2.circle(frame, (index_x, index_y), radius=8 , color=(255, 0, 0), thickness=2)

    # Face mesh for eye-controlled clicking
    if landmarks_points:
        landmarks = landmarks_points[0].landmark
        
        # Get the necessary landmarks for the left eye (upper and lower eyelids)
        left_eye_upper = landmarks[145]
        left_eye_lower = landmarks[159]

        # Calculate the pixel positions of these landmarks
        left_eye_upper_y = left_eye_upper.y * frame_h
        left_eye_lower_y = left_eye_lower.y * frame_h

        # Check if the eye is closed enough to trigger a click
        eye_distance = left_eye_upper.y - left_eye_lower.y
        if eye_distance < 0.015:  # Adjust this threshold based on your testing
            eye_closed_time += time.time() - previous_time
            
            # Check if the closure time exceeds the threshold and is not already clicking
            if eye_closed_time >= click_threshold and not is_clicking:
                click_times.append(current_time)  # Log the click time
                is_clicking = True  # Mark that a click has occurred
                eye_closed_time = 0  # Reset timer after clicking
                
                # Check for double click
                if len(click_times) >= 2 and (click_times[-1] - click_times[-2]) <= double_click_threshold:
                    pyautogui.doubleClick()  # Perform double click
                    click_times.clear()  # Clear the click times after a double click
                else:
                    pyautogui.click()  # Single click
        else:
            eye_closed_time = 0  # Reset if eye is open
            is_clicking = False  # Reset clicking state

    # Display the frame with drawn landmarks
    cv2.imshow('Virtual Mouse with Eye Click', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    previous_time = current_time  # Update previous time

# Release the camera and close windows
cam.release()
cv2.destroyAllWindows()

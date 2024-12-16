import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import time
from math import sqrt
import pywintypes
import pythoncom
import win32api
import pyautogui


# Initialize variables
click = 0
video = cv2.VideoCapture(0)

# Initialize MediaPipe hands and drawing modules
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Start capturing video and processing hands
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        # Capture video frame
        ret, frame = video.read()
        if not ret:
            break

        # Convert the frame color to RGB and flip it for a mirror effect
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        imageHeight, imageWidth, _ = image.shape

        # Process the image to find hands
        results = hands.process(image)
        
        # Convert the image color back to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw hand landmarks if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )

                # Initialize variables for fingertip coordinates
                indexfingertip_x = indexfingertip_y = None
                thumbfingertip_x = thumbfingertip_y = None

                # Loop through each hand landmark to find specific points
                for point in mp_hands.HandLandmark:
                    normalized_landmark = hand_landmarks.landmark[point]
                    pixel_coordinates_landmark = mp_drawing._normalized_to_pixel_coordinates(
                        normalized_landmark.x, normalized_landmark.y, imageWidth, imageHeight
                    )

                    if pixel_coordinates_landmark is not None:
                        # Convert point to string for comparison
                        point_str = str(point)

                        # Check for index finger tip
                        if point_str == "HandLandmark.INDEX_FINGER_TIP":
                            indexfingertip_x, indexfingertip_y = pixel_coordinates_landmark
                            try:
                                win32api.SetCursorPos((indexfingertip_x * 4, indexfingertip_y * 5))
                            except:
                                pass

                        # Check for thumb tip
                        elif point_str == "HandLandmark.THUMB_TIP":
                            thumbfingertip_x, thumbfingertip_y = pixel_coordinates_landmark

                # Calculate the distance between the index fingertip and thumb tip if both are detected
                if indexfingertip_x is not None and thumbfingertip_x is not None:
                    try:
                        distance_x = sqrt((indexfingertip_x - thumbfingertip_x) ** 2)
                        distance_y = sqrt((indexfingertip_y - thumbfingertip_y) ** 2)
                        # Add any additional code to handle these distances, e.g., to trigger a click
                    except:
                        pass

        # Display the resulting frame
        cv2.imshow("Hand Tracking", image)

        # Press 'q' to exit the loop
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release resources
video.release()
cv2.destroyAllWindows()

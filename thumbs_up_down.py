import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Define the screen dimensions (width and height)
screen_width = 1920  
screen_height = 1080  

# Initialize the previous Y positions for fingers
prev_y_positions = [0] * 5

# Capture video from your camera (you may need to adjust the source)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hand landmarks
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            for i, landmark in enumerate(landmarks.landmark):
                x, y, z = landmark.x, landmark.y, landmark.z  # Get 3D coordinates

                # Adjust x and y positions to screen dimensions
                x_pos = int(x * screen_width)
                y_pos = int(y * screen_height)

                # Draw blue colored circles around the fingertips
                if i in [4, 8, 12, 16, 20]:
                    cv2.circle(frame, (x_pos, y_pos), 10, (255, 0, 0), -1)

                # Check if the finger is folded
                if i == 0:
                    finger_fold_status = [True]
                else:
                    # Check if the X position of the current finger tip is smaller than the previous finger tip
                    if x < landmarks.landmark[i - 1].x:
                        # Draw a green circle at the tip
                        cv2.circle(frame, (x_pos, y_pos), 10, (0, 255, 0), -1)
                        finger_fold_status.append(True)
                    else:
                        finger_fold_status.append(False)

        # Check if all fingers are folded
        if all(finger_fold_status):
            # Check if the thumb is raised up
            if landmarks.landmark[4].y < prev_y_positions[0]:
                print("LIKE")
                cv2.putText(frame, "LIKE", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Add similar conditions for "DISLIKE" here

    # Update the previous Y positions
    prev_y_positions = [landmarks.landmark[4].y]

    # Show the frame with circles and text
    cv2.imshow("Hand Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the VideoCapture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Close MediaPipe Hands
hands.close()

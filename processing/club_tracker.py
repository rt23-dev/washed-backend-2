import cv2
import numpy as np
import json

def track_club(video_path, output_json_path):
    cap = cv2.VideoCapture(video_path)
    trail = []
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
    
        frame_idx += 1
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        clubhead = None
        if contours:
            largest = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                clubhead = (cX, cY)
        
        if clubhead:
            trail.append({
                "frame": frame_idx,
                "clubhead": {
                    "x": clubhead[0],
                    "y": clubhead[1]
                }
            })
    
    cap.release()
    with open(output_json_path, "w") as f:
        json.dump(trail, f)

    print(f"[Club Tracker] Extracted {len(trail)} frames of clubhead positions.")
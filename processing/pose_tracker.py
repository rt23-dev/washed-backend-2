import cv2
import mediapipe as mp
import json

mp_pose = mp.solutions.pose

def extract_pose_landmarks(video_path, output_json_path):
    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose(static_image_mode=False)
    
    all_landmarks = []
    frame_idx = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_idx += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            frame_landmarks = []
            for lm in results.pose_landmarks.landmark:
                frame_landmarks.append({
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z,
                    "visibility": lm.visibility
                })
            all_landmarks.append({
                "frame": frame_idx,
                "landmarks": frame_landmarks
            })

    pose.close()
    cap.release()

    with open(output_json_path, "w") as f:
        json.dump(all_landmarks, f)
    
    print(f"[Pose] Extracted {len(all_landmarks)} frames of landmarks.")
    

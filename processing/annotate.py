import json
import cv2
import os

def render_annotated_video(video_path, pose_path, club_path, output_path):
    # Load pose and club data
    with open(pose_path, "r") as f:
        pose_data = json.load(f)

    with open(club_path, "r") as f:
        club_data = json.load(f)

    # Map frames to pose landmarks and club positions
    pose_map = {item["frame"]: item["landmarks"] for item in pose_data}
    club_map = {item["frame"]: item["clubhead"] for item in club_data}

    # Open original video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 1  # Frames in your data are 1-indexed
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Draw pose landmarks if available
        if frame_idx in pose_map:
            for lm in pose_map[frame_idx]:
                x = int(lm["x"] * width)
                y = int(lm["y"] * height)
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        # Draw clubhead if available
        if frame_idx in club_map:
            club_x = int(club_map[frame_idx]["x"])
            club_y = int(club_map[frame_idx]["y"])
            cv2.circle(frame, (club_x, club_y), 6, (0, 0, 255), -1)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print(f"[Visualization] Saved annotated video to {output_path}")

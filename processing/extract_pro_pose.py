import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from processing.pose_tracker import extract_pose_landmarks
from processing.club_tracker import track_club

if __name__ == "__main__":
    extract_pose_landmarks(
        "pro/pro_golf_swing.mp4",
        "pro/pro_golf_swing_pose.json"
    )
    track_club(
        "pro/pro_golf_swing.mp4",
        "pro/pro_golf_swing_club.json"
    )
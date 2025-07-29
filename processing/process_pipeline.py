import time
import json
import os
from processing.pose_tracker import extract_pose_landmarks
from processing.club_tracker import track_club
from processing.compare import compare_swing
from gpt.generate_feedback import generate_feedback
from processing.annotate import render_annotated_video

def process_session(session_id, video_path, output_dir):
    print(f"[{session_id}] Starting processing...", flush=True)
    start = time.time()

    pose_path = os.path.join(output_dir, f"{session_id}_pose.json")
    club_path = os.path.join(output_dir, f"{session_id}_club.json")

    extract_pose_landmarks(video_path, pose_path)
    track_club(video_path, club_path)

    annotated_video_path = os.path.join(output_dir, f"{session_id}_annotated.mp4")
    render_annotated_video(video_path, pose_path, club_path, annotated_video_path)

    pro_pose = "pro/pro_golf_swing_pose.json"
    pro_club = "pro/pro_golf_swing_club.json"
    score_path = os.path.join(output_dir, f"{session_id}_score.json")

    compare_swing(pose_path, club_path, pro_pose, pro_club, score_path)

    with open(score_path, 'r') as f:
        score_data = json.load(f)

    # GPT-generated tips
    tips = generate_feedback(score_data)

    feedback = {
    "session_id": session_id,
    "pose_score": score_data.get("pose_score"),
    "club_score": score_data.get("club_score"),
    "overall_score": score_data.get("overall_score"),
    "text": tips,
    "video_url": f"/mock_outputs/{session_id}_annotated.mp4"
}
    feedback_path = os.path.join(output_dir, f"{session_id}_feedback.json")
    with open(feedback_path, 'w') as f:
        json.dump(feedback, f)
        f.flush()
        os.fsync(f.fileno())

    meta_path = os.path.join(output_dir, f"{session_id}_meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            metadata = json.load(f)
        metadata['status'] = 'processed'
        with open(meta_path, 'w') as f:
            json.dump(metadata, f)
            f.flush()
            os.fsync(f.fileno())

    end = time.time()
    print(f"[{session_id}] Processing complete in {end - start:.2f}s. Feedback saved.", flush=True)

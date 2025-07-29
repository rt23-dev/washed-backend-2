import json
import numpy as np
from scipy.spatial.distance import euclidean

def extract_right_elbow_angle(landmarks):
    def angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        ba = a - b
        bc = c - b
        cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-5)
        return np.arccos(np.clip(cosine, -1.0, 1.0)) * 180 / np.pi
    
    try:
        shoulder = landmarks[12]
        elbow = landmarks[14]
        wrist = landmarks[16]
        return angle(
            (shoulder['x'], shoulder['y']),
            (elbow['x'], elbow['y']),
            (wrist['x'], wrist['y'])
        )
    except:
        return None
    
def compare_pose(user_path, pro_path):
    with open(user_path, 'r') as f:
        user_data = json.load(f)
    with open(pro_path, 'r') as f:
        pro_data = json.load(f)
    
    n = min(len(user_data), len(pro_data))
    diffs = []

    for i in range(n):
        user_angle = extract_right_elbow_angle(user_data[i]['landmarks'])
        pro_angle = extract_right_elbow_angle(pro_data[i]['landmarks'])
        if user_angle is not None and pro_angle is not None:
            diff = abs(user_angle - pro_angle)
            diffs.append(diff)

    if not diffs:
        return 0
    
    avg_diff = np.mean(diffs)
    return max(0, 100 - avg_diff)  # Ensure the score is between 0 and 100

def compare_club(user_path, pro_path):
    with open(user_path, 'r') as f:
        user_data = json.load(f)
    with open(pro_path, 'r') as f:
        pro_data = json.load(f)
    
    n = min(len(user_data), len(pro_data))
    diffs = []

    for i in range(n):
        user_clubhead = user_data[i]['clubhead']
        pro_clubhead = pro_data[i]['clubhead']
        diff = euclidean(
            (user_clubhead['x'], user_clubhead['y']),
            (pro_clubhead['x'], pro_clubhead['y'])
        )
        diffs.append(diff)

    if not diffs:
        return 0
    
    avg_diff = np.mean(diffs)
    max_dist = 300
    return max(0, 100 - (avg_diff / max_dist * 100))  # Ensure the score is between 0 and 100

def compare_swing(user_pose, pro_club, pro_pose, user_club, output_path):
    pose_score = compare_pose(user_pose, pro_pose)
    club_score = compare_club(user_club, pro_club)

    overall = round(0.6 * pose_score + 0.4 * club_score, 2)

    result = {
        "pose_score": round(pose_score, 2),
        "club_score": round(club_score, 2),
        "overall_score": overall
    }

    with open(output_path, 'w') as f:
        json.dump(result, f)

    print(f"[Comparison] Pose Score: {pose_score:.2f}, Club Score: {club_score:.2f}, Overall Score: {overall:.2f}")
    return result
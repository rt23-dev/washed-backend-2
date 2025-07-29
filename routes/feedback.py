import os
import json
from flask import Blueprint, jsonify

feedback_bp = Blueprint('feedback', __name__)
UPLOAD_FOLDER = os.getenv('UPLOAD_DIR', 'uploads')

@feedback_bp.route('/feedback/<session_id>', methods=['GET'])
def get_feedback(session_id):
    feedback_path = os.path.join(UPLOAD_FOLDER, f"{session_id}_feedback.json")
    
    if not os.path.exists(feedback_path):
        return jsonify({"status":"processing"}), 202
    
    with open(feedback_path, 'r') as f:
        feedback = json.load(f)
    
    return jsonify(feedback), 200
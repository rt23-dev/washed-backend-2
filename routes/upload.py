from concurrent.futures import thread
import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import json
from datetime import datetime
import threading
from processing.process_pipeline import process_session

load_dotenv()

upload_bp = Blueprint('upload', __name__)
UPLOAD_FOLDER = os.getenv('UPLOAD_DIR', 'uploads')
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["video"]
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    session_id = request.form.get("session_id")
    if not session_id: 
        session_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, session_id + "_" + filename)
    file.save(save_path)

    metadata = {
        "session_id": session_id,
        "filename": filename,
        "upload_path": save_path,
        "created_at": datetime.now().isoformat(),
        "status": "uploaded"
    }

    with open(os.path.join(UPLOAD_FOLDER, session_id + ".json"), 'w') as f:
        json.dump(metadata, f)

    # Background processing
    thread = threading.Thread(
    target=process_session,
    args=(session_id, save_path, UPLOAD_FOLDER),
    daemon=True  # ensures thread exits cleanly with Flask
    )
    thread.start()

    return jsonify({"session_id": session_id}), 200


from flask import Flask, render_template, Response, jsonify, send_from_directory
import os
import cv2
import json
import sqlite3
from alert_system.database import get_latest_alerts

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(os.path.dirname(BASE_DIR), "tracking", "Data", "cctv.mp4")
EVIDENCE_DIR = os.path.join(os.path.dirname(BASE_DIR), "evidence")

@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('dashboard.html')

@app.route('/evidence')
def evidence_gallery():
    """Render the evidence gallery."""
    files = []

    # List files in main evidence dir
    try:
        root_files = [f for f in os.listdir(EVIDENCE_DIR) if os.path.isfile(os.path.join(EVIDENCE_DIR, f))]
        files.extend(root_files)
    except FileNotFoundError:
        pass

    # Include snapshots and videos subfolders if present
    for sub in ("snapshots", "videos"):
        subdir = os.path.join(EVIDENCE_DIR, sub)
        if os.path.isdir(subdir):
            for f in os.listdir(subdir):
                if f.lower().endswith(('.mp4', '.jpg', '.jpeg', '.png')):
                    files.append(os.path.join(sub, f))

    # Sort reverse chronological by filename (timestamps are used in names)
    evidence_files = sorted(files, reverse=True)
    return render_template('evidence.html', files=evidence_files)

@app.route('/evidence/file/<path:filepath>')
def get_evidence_file(filepath):
    """Serve evidence file from evidence dir or its subfolders."""
    dirpart, fname = os.path.split(filepath)
    target_dir = EVIDENCE_DIR if not dirpart else os.path.join(EVIDENCE_DIR, dirpart)
    return send_from_directory(target_dir, fname)

@app.route('/api/alerts')
def api_alerts():
    """API to get latest alerts for the dashboard."""
    alerts = get_latest_alerts(limit=10)
    # Convert rows to dicts if needed, depending on how template uses them or JS uses them
    return jsonify(alerts)

def gen_frames():
    """Generator for video streaming (Simulate Live Feed from the recorded video)."""
    cap = cv2.VideoCapture(VIDEO_PATH)
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop video
            continue
        
        # We could add bounding boxes here if we ran detection in real-time or synced with output.json
        # For this dashboard demo, we just show the raw feed per requirements/simplicity
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

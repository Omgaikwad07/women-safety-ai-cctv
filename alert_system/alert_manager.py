# alert_system/alert_manager.py

import os
import json
import cv2
from .database import init_db, save_alert
from .evidence_storage import save_snapshot, save_video

THREAT_THRESHOLD = 0.7


def check_threat(threat_score):
    return threat_score >= THREAT_THRESHOLD


def process_behavior_output():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    behavior_path = os.path.join(base_dir, "behavior_analysis", "outputs", "behavior_output.json")
    video_path = os.path.join(base_dir, "tracking", "Data", "cctv.mp4")

    if not os.path.exists(behavior_path):
        print("No behavior output found at", behavior_path)
        return

    with open(behavior_path) as f:
        data = json.load(f)

    # Ensure DB is ready
    init_db()

    cap = None

    for item in data:
        score = item.get("threat_score", 0)
        if not check_threat(score):
            continue

        frames = item.get("violation_frames", []) or []

        # For the first violation frame, extract evidence (snapshot + short clip)
        for fid in frames:
            if not isinstance(fid, int) or fid < 0:
                continue

            try:
                if cap is None:
                    cap = cv2.VideoCapture(video_path)
                    if not cap.isOpened():
                        print("Unable to open video for evidence extraction:", video_path)
                        cap = None
                        break

                fps = cap.get(cv2.CAP_PROP_FPS) or 20
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

                # Clamp frame index
                frame_idx = min(max(0, fid), max(0, total_frames - 1))

                # Snapshot
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read frame", frame_idx)
                    continue

                snapshot_path = save_snapshot(frame)

                # Short clip around the violation frame: 15 frames before and after
                start = max(0, frame_idx - 15)
                end = min(total_frames - 1, frame_idx + 15)

                frames_clip = []
                cap.set(cv2.CAP_PROP_POS_FRAMES, start)
                for f in range(start, end + 1):
                    retc, fr = cap.read()
                    if not retc:
                        break
                    frames_clip.append(fr)

                video_path_saved = None
                if frames_clip:
                    video_path_saved = save_video(frames_clip, fps=max(1, int(fps)))

                save_alert(score, snapshot_path, video_path_saved)

                print(f"Alert created (score={score}) snapshot={snapshot_path} video={video_path_saved}")
                # Only capture the first relevant frame per item to avoid duplicates
                break

            except Exception as e:
                print("Error extracting evidence:", e)

    if cap:
        cap.release()


if __name__ == "__main__":
    process_behavior_output()

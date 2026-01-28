import cv2
import json
from detector import detect_persons
from stream_reader import get_video_stream
from tracker import CentroidTracker

# -------- Camera Inputs --------
camera_sources = {
    "cam1": "cctv.mp4"
    # Add more if needed
}

caps = {}
trackers = {}
frame_ids = {}
outputs = {}
stream_active = {}

for cam_id, src in camera_sources.items():
    caps[cam_id] = get_video_stream(src)
    trackers[cam_id] = CentroidTracker()
    frame_ids[cam_id] = 0
    outputs[cam_id] = []
    stream_active[cam_id] = True

# -------- Main Loop --------
while True:
    all_streams_finished = True

    for cam_id, cap in caps.items():
        if not stream_active[cam_id]:
            continue

        ret, frame = cap.read()

        if not ret:
            stream_active[cam_id] = False
            continue

        all_streams_finished = False
        frame_ids[cam_id] += 1

        # Detect persons
        persons = detect_persons(frame)
        detections = [(x1,y1,x2,y2) for (x1,y1,x2,y2,conf) in persons]

        # Track persons
        tracked = trackers[cam_id].update(detections)

        frame_records = []

        for person_id, (x1,y1,x2,y2,cx,cy) in tracked.items():
            w = x2 - x1
            h = y2 - y1

            # Optional display
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame,f"{cam_id} ID:{person_id}",
                        (x1,y1-5),cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,(0,255,0),1)

            # Save record
            frame_records.append({
                "camera_id": cam_id,
                "frame_id": frame_ids[cam_id],
                "person_id": person_id,
                "bounding_box": {"x": x1, "y": y1, "w": w, "h": h},
                "centroid": {"cx": cx, "cy": cy}
            })

        outputs[cam_id].append(frame_records)

        # Display
        frame_resized = cv2.resize(frame, (640, 360))
        cv2.imshow(f"Human Detection - {cam_id}", frame_resized)

    if all_streams_finished:
        break

    if cv2.waitKey(1) & 0xFF == 27:
        break

# -------- Cleanup --------
for cap in caps.values():
    cap.release()
cv2.destroyAllWindows()

# -------- Save Outputs Properly --------
for cam_id, data in outputs.items():
    filename = f"output_{cam_id}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Output saved: {filename}")

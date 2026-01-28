# import cv2
# import json
# from detector import detect_persons
# from stream_reader import get_video_stream
# from tracker import CentroidTracker
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
# OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.json")

# os.makedirs(OUTPUT_DIR, exist_ok=True)
# cap = get_video_stream("cctv.mp4")

# tracker = CentroidTracker()
# frame_id = 0

# output_data = []  # List of per-frame records

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame_id += 1

#     # Detect persons
#     persons = detect_persons(frame)

#     # Extract only bounding boxes
#     detections = [(x1,y1,x2,y2) for (x1,y1,x2,y2,conf) in persons]

#     # Track persons & assign IDs
#     tracked = tracker.update(detections)

#     frame_records = []

#     for person_id, (x1,y1,x2,y2,cx,cy) in tracked.items():
#         w = x2 - x1
#         h = y2 - y1

#         # Draw on frame (optional display)
#         cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
#         cv2.putText(frame,f"ID {person_id}",(x1,y1-5),
#                     cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

#         # Save record
#         frame_records.append({
#             "frame_id": frame_id,
#             "person_id": person_id,
#             "bounding_box": {"x": x1, "y": y1, "w": w, "h": h},
#             "centroid": {"cx": cx, "cy": cy}
#         })

#     output_data.append(frame_records)

#     # Display resized
#     frame_resized = cv2.resize(frame, (960,540))
#     cv2.imshow("Human Detection CCTV", frame_resized)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()

# # Save output to JSON file
# with open(OUTPUT_FILE, "w") as f:
#     json.dump(output_data, f, indent=4)

# print("✅ Detection output saved to output.json")


import cv2
import json
from detector import detect_persons
from stream_reader import get_video_stream
from tracker import CentroidTracker
import os

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIDEO_PATH = os.path.join(BASE_DIR, "data", "cctv.mp4")  # <-- FIX 1
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- CLEAR OLD OUTPUT ----------------
if os.path.exists(OUTPUT_FILE):              # <-- FIX 2
    os.remove(OUTPUT_FILE)

# ---------------- VIDEO STREAM ----------------
cap = get_video_stream(VIDEO_PATH)

# ---------------- TRACKER RESET PER RUN ----------------
tracker = CentroidTracker()
frame_id = 0
output_data = []  # per-frame records

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    print("Frame read:", ret)

    if not ret:
        break

    frame_id += 1

    # Detect persons
    persons = detect_persons(frame)
    print("Detections:", len(persons))


    # Extract bounding boxes only
    detections = [(x1, y1, x2, y2) for (x1, y1, x2, y2, conf) in persons]

    # Track persons
    tracked = tracker.update(detections)

    frame_records = []

    for person_id, (x1, y1, x2, y2, cx, cy) in tracked.items():
        w = x2 - x1
        h = y2 - y1

        # Draw (optional)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"ID {person_id}",
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        # Save record
        frame_records.append({
            "frame_id": frame_id,
            "person_id": person_id,
            "bounding_box": {"x": x1, "y": y1, "w": w, "h": h},
            "centroid": {"cx": cx, "cy": cy}
        })

    output_data.append(frame_records)

    # # Display
    # frame_resized = cv2.resize(frame, (960, 540))
    # cv2.imshow("Human Detection CCTV", frame_resized)

    # if cv2.waitKey(1) & 0xFF == 27:
    #     break

cap.release()
cv2.destroyAllWindows()

# ---------------- SAVE JSON ----------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(output_data, f, indent=4)

print("✅ Detection output saved to tracking/outputs/output.json")

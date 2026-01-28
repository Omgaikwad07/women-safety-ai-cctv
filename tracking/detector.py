from ultralytics import YOLO

# Load YOLOv8 pretrained model
model = YOLO("yolov8n.pt")  # nano = fastest

def detect_persons(frame):
    results = model(frame, verbose=False)
    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == 0:  # COCO class 0 = person
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                detections.append((x1,y1,x2,y2,conf))
    
    return detections

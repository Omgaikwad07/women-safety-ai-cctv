## Tracking Output Contract (Person 2 → Person 3)

Each detected person per frame is stored as JSON:

{
  "frame_id": 120,
  "timestamp": "00:00:04.80",
  "person_id": 3,
  "bbox": [x, y, w, h],
  "centroid": [cx, cy],
  "confidence": 0.89
}

- person_id is consistent across frames
- bbox format: [x, y, width, height]
- centroid = center of bbox

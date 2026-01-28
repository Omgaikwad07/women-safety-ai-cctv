import math

class CentroidTracker:
    def __init__(self, max_distance=50):
        self.next_person_id = 0
        self.objects = {}  # person_id -> (centroid_x, centroid_y)
        self.max_distance = max_distance

    def update(self, detections):
        # detections = list of (x1,y1,x2,y2)

        new_objects = {}
        assigned_ids = {}

        for (x1, y1, x2, y2) in detections:
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            matched_id = None
            min_dist = float("inf")

            for person_id, (px, py) in self.objects.items():
                dist = math.hypot(cx - px, cy - py)
                if dist < min_dist and dist < self.max_distance:
                    min_dist = dist
                    matched_id = person_id

            if matched_id is None:
                matched_id = self.next_person_id
                self.next_person_id += 1

            new_objects[matched_id] = (cx, cy)
            assigned_ids[matched_id] = (x1, y1, x2, y2, cx, cy)

        self.objects = new_objects
        return assigned_ids

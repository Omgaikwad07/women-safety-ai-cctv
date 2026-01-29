import json
from collections import defaultdict
from utils import euclidean, movement_vector, cosine_similarity
import rules
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_PATH = os.path.join(
    BASE_DIR, "tracking", "outputs", "output.json"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "behavior_analysis", "outputs", "behavior_output.json"
)

def speed(prev, curr):
    return ((curr['cx'] - prev['cx'])**2 + (curr['cy'] - prev['cy'])**2) ** 0.5


def load_data():
    with open(INPUT_PATH) as f:
        return json.load(f)

def analyze():
    data = load_data()

    proximity_counter = defaultdict(int)
    follow_counter = defaultdict(int)
    aggressive_counter = defaultdict(int)
    threat_scores = defaultdict(int)
    reason_tracker = defaultdict(list)

 

    prev_frame = {}

    for frame in data:
        current = {p["person_id"]: p["centroid"] for p in frame}

        ids = list(current.keys())

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = ids[i], ids[j]
                dist = euclidean(current[a], current[b])

                pair = tuple(sorted((a, b)))

                # Proximity
                if dist < rules.PROXIMITY_DISTANCE:
                    proximity_counter[pair] += 1
                else:
                    proximity_counter[pair] = 0

                if proximity_counter[pair] == rules.PROXIMITY_FRAMES:
                    threat_scores[pair] += 30
                    reason_tracker[pair].append("Proximity Violation")

                # Aggressive Movement Detection
                if a in prev_frame and b in prev_frame:
                    prev_dist = euclidean(prev_frame[a], prev_frame[b])
                    curr_dist = euclidean(current[a], current[b])

                    speed_a = speed(prev_frame[a], current[a])

                    # Sudden fast movement + closing distance
                    if (
                        speed_a > rules.AGGRESSIVE_SPEED_THRESHOLD and
                        (prev_dist - curr_dist) > rules.AGGRESSIVE_DISTANCE_DROP
                    ):
                        aggressive_counter[pair] += 1
                    else:
                        aggressive_counter[pair] = 0

                    if aggressive_counter[pair] == rules.AGGRESSIVE_FRAMES:
                        threat_scores[pair] += 50
                        reason_tracker[pair].append("Aggressive Movement")


                # Following
                if a in prev_frame and b in prev_frame:
                    va = movement_vector(prev_frame[a], current[a])
                    vb = movement_vector(prev_frame[b], current[b])
                    if cosine_similarity(va, vb) > 0.8 and dist < rules.FOLLOW_DISTANCE:
                        follow_counter[pair] += 1
                    else:
                        follow_counter[pair] = 0

                    if follow_counter[pair] == rules.FOLLOW_FRAMES:
                        threat_scores[pair] += 40
                        reason_tracker[pair].append("Following Detected")


        prev_frame = current

    output = []
    for pair, score in threat_scores.items():
        level = "LOW"
        if score >= 60:
            level = "HIGH"
        elif score >= 30:
            level = "MEDIUM"

        output.append({
            "pair": pair,
            "threat_score": score,
            "threat_level": level,
            "reasons": reason_tracker.get(pair, [])
        })


    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print("Behavior analysis completed.")

if __name__ == "__main__":
    analyze()

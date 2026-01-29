import math

def euclidean(p1, p2):
    return math.sqrt((p1['cx'] - p2['cx'])**2 + (p1['cy'] - p2['cy'])**2)

def movement_vector(prev, curr):
    return (curr['cx'] - prev['cx'], curr['cy'] - prev['cy'])

def cosine_similarity(v1, v2):
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
    if mag1 == 0 or mag2 == 0:
        return 0
    return dot / (mag1 * mag2)

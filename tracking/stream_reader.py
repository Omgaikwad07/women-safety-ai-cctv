import cv2

def get_video_stream(source):
    cap = cv2.VideoCapture(source)  # source can be 0 or RTSP link
    return cap

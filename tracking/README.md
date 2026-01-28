Human Detection Module – Output Interface Documentation
Module Purpose

This module detects humans in CCTV footage and outputs structured per-frame detection data.
The output is designed to be used as input for the next module (behavior analysis, tracking, event detection, etc.).

Input to This Module

• Video file (cctv.mp4) or CCTV RTSP stream
• No prior annotations required

Output File

After execution, the module generates:

output.json

Output JSON Structure

Each frame produces a list of detected persons.

Example:

[
  [
    {
      "frame_id": 1,
      "person_id": 0,
      "bounding_box": { "x": 412, "y": 210, "w": 85, "h": 190 },
      "centroid": { "cx": 454, "cy": 305 }
    },
    {
      "frame_id": 1,
      "person_id": 1,
      "bounding_box": { "x": 620, "y": 180, "w": 90, "h": 200 },
      "centroid": { "cx": 665, "cy": 280 }
    }
  ],

  [
    {
      "frame_id": 2,
      "person_id": 0,
      "bounding_box": { "x": 418, "y": 212, "w": 85, "h": 190 },
      "centroid": { "cx": 460, "cy": 307 }
    }
  ]
]

Meaning of Each Field
Field	Description
frame_id	Sequential frame number
person_id	Unique ID assigned to each person, consistent across frames
bounding_box (x,y,w,h)	Top-left coordinate + width & height
centroid (cx,cy)	Center point of bounding box
How Next Module Should Use This

The next module can:

• Read output.json
• Loop per frame
• Access each person’s bounding box
• Use centroid trajectory for behavior / motion analysis

Example Prompt for Next Developer

"Read output.json. For each frame, use person_id to track motion paths across frames. Use centroid coordinates to compute speed or detect abnormal behavior."

Multi-Camera Input Support
Input Format

Define multiple camera feeds in multi_main.py:

camera_sources = {
   "cam1": "cctv1.mp4",
   "cam2": "cctv2.mp4"
}


Each entry represents one camera feed.
The key name becomes the camera_id in the output.

Output Files

Each camera produces its own structured output:

output_cam1.json
output_cam2.json

Output Record Structure
{
  "camera_id": "cam1",
  "frame_id": 12,
  "person_id": 0,
  "bounding_box": { "x": 420, "y": 210, "w": 80, "h": 190 },
  "centroid": { "cx": 460, "cy": 305 }
}

How Next Module Uses This

The next module simply:

• Loads each output_camX.json
• Processes per camera separately
• Uses person_id + centroid trajectories
• Performs behavior or event analysis

✅ Why This Design Works

✔ Supports unlimited camera feeds
✔ Real-time multi-stream processing
✔ Independent tracking per camera
✔ Clean structured outputs
✔ Easy to scale later

🚀 Optional Professional Upgrade (Later)

• True multi-threaded processing
• GPU batch inference
• DeepSORT tracking
• Centralized database output
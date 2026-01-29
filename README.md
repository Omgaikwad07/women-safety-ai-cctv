🛡️ Women Safety AI CCTV System

An AI-based CCTV analytics system designed to enhance women safety by detecting humans, tracking their movement, analyzing suspicious behavior, and generating threat insights using computer vision and rule-based logic.

The system is designed to work with:

Recorded CCTV videos

Live webcam

Live IP CCTV streams (RTSP)

📂 Project Structure
women-safety-ai-cctv/
│
├── tracking/                  
│   ├── main.py                # Detection + tracking runner
│   ├── detector.py
│   ├── tracker.py
│   ├── stream_reader.py
│   ├── data/
│   │   └── cctv.mp4            # Input video
│   └── outputs/
│       └── output.json         # Tracking output (input for behavior analysis)
│
├── behavior_analysis/        
│   ├── behavior_analysis.py
│   └── utils.py
|   └── rules.py
|   └── outputs/
│       └──behavior_output.json  
│
├── requirements.txt            # Full project dependencies
└── README.md

⚙️ System Requirements

Python: 3.8 or higher

OS: Windows / Linux / macOS

Recommended: GPU (optional, CPU works for demo)

📦 Installation (One-Time Setup)
1️⃣ Clone the repository
git clone https://github.com/Omgaikwad07/women-safety-ai-cctv.git
cd women-safety-ai-cctv

2️⃣ Install dependencies
python -m pip install -r requirements.txt


On Windows (recommended):

py -3.11 -m pip install -r requirements.txt

▶️ How to Run the Entire Project (Step-by-Step)
🔹 STEP 1: Run Detection & Tracking 

This step:

Reads CCTV / video input

Detects humans using YOLO

Tracks each person across frames

Generates structured JSON output

python tracking/main.py


📌 Output generated at:

tracking/outputs/output.json


This file contains per-frame, per-person:

person_id

bounding box

centroid coordinates

🔹 STEP 2: Run Behavior Analysis

This step:

Reads output.json

Analyzes behavior such as:

Proximity violation

Following patterns

Aggressive Behavior

Assigns threat levels (Low / Medium / High)

python behavior_analysis/behavior_analysis.py


📌 Output:

Generates behavior_output.json containing threat details

🔁 Running with Different Video Sources
▶️ Recorded Video

Replace video inside:

tracking/data/cctv.mp4

▶️ Webcam

In stream_reader.py:

cv2.VideoCapture(0)

▶️ Live CCTV (RTSP)
cv2.VideoCapture("rtsp://username:password@ip:port/stream")


No other code changes required.

🧠 Key Design Highlights

Modular architecture (each person owns one module)

Branch-based GitHub workflow

Rule-based behavior analysis (simple & explainable)

Real-time capable (hardware dependent)

Clean JSON interface between modules
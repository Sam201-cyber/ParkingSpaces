🚗 Car Parking Space Counter
An intelligent, real-time car parking management system built using FastAPI, WebSockets, and Computer Vision. The system detects and tracks available parking slots, updates clients in real time, and exposes a REST API for metadata. It's designed for use in smart cities, commercial parking lots, campuses, and more.

📚 Table of Contents
Features

Use Cases

Architecture

Tech Stack

Requirements

Setup & Installation

Project Files

API and WebSocket

Demo

Future Enhancements

References

License

🌟 Features
✅ Real-time tracking of parking slot occupancy

🔌 WebSocket-based real-time communication with frontend clients

📡 REST API to fetch parking metadata (available, occupied slots, etc.)

🎥 Camera/video input for slot monitoring (via OpenCV or YOLO integration)

🧠 Configurable parking slot picker using mouse (manual mode)

🌐 Responsive web interface built with HTML & JavaScript

🚀 Built with FastAPI for performance and scalability

🧠 Use Cases
🏙 Smart city parking solutions

🏢 Office or mall parking lot management

🏫 University or school campus parking

🅿️ Apartment or gated community parking monitoring

📊 Data analytics on parking behavior and usage

🏗 Architecture
text
Copy
Edit
Camera / Video Feed
      │
      ▼
[ parkingspacepicker.py ]
(Detect or manually pick parking regions)
      │
      ▼
[ main.py ]
- FastAPI backend
- WebSocket server
- REST API for metadata
      │
      ▼
[ templates/index.html ]
- Connects to WebSocket
- Shows real-time parking updates to users
🛠 Tech Stack
Python 3.11+

FastAPI - for the backend API

WebSockets - real-time updates

OpenCV - optional CV-based input

HTML/CSS/JavaScript - frontend

Uvicorn - ASGI server

📦 Requirements
File: requirements.txt

nginx
Copy
Edit
fastapi
uvicorn
opencv-python
jinja2
Install them with:

bash
Copy
Edit
pip install -r requirements.txt
⚙️ Setup & Installation
Clone the repo

bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/parking-space.git
cd parking-space
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the app

bash
Copy
Edit
uvicorn main:app --reload
Open in browser

Visit: http://localhost:8000

📁 Project Files
🔹 main.py
Handles the backend:

Serves the frontend (index.html)

Provides /metadata REST endpoint

Manages WebSocket connections (/ws)

Broadcasts slot updates to clients

Key Endpoints:
GET / – loads the HTML UI

GET /metadata – returns JSON metadata

WebSocket /ws – pushes real-time updates to clients

python
Copy
Edit
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

connected_clients = []

metadata = {
    "total_slots": 50,
    "occupied_slots": 18,
    "available_slots": 32,
    "last_updated": datetime.datetime.now().isoformat()
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/metadata")
async def get_metadata():
    return metadata

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # We don't use incoming messages here
    except:
        connected_clients.remove(websocket)

# Function to broadcast updates to all clients
async def broadcast_update(data: dict):
    for ws in connected_clients:
        await ws.send_json({"event": "update", "data": data})
🔹 parkingspacepicker.py
Tool to manually mark parking slot regions using OpenCV. This allows you to configure static parking lots where slot locations are fixed.

Features:
Use mouse to draw rectangles on a video frame

Save parking region data to file for later use

Example Usage:
python
Copy
Edit
import cv2

# Load a video frame or image
frame = cv2.imread("parking_lot.jpg")

# Use OpenCV to mark parking slots
# (Implement drawing and saving logic)
In a real application, you’d integrate this with YOLO or use pre-defined coordinates.

🔹 templates/index.html
Simple web UI to connect to the backend WebSocket and display updates.

index.html Example:
html
Copy
Edit
<!DOCTYPE html>
<html>
<head>
  <title>Parking Space Counter</title>
</head>
<body>
  <h1>Parking Monitor</h1>
  <p>Occupied: <span id="occupied">--</span></p>
  <p>Available: <span id="available">--</span></p>

  <script>
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = function(event) {
      const msg = JSON.parse(event.data);
      if (msg.event === "update") {
        document.getElementById("occupied").textContent = msg.data.occupied;
        document.getElementById("available").textContent = msg.data.available;
      }
    };
  </script>
</body>
</html>
🔌 API and WebSocket
GET /metadata
Returns:

json
Copy
Edit
{
  "total_slots": 50,
  "occupied_slots": 18,
  "available_slots": 32,
  "last_updated": "2025-08-07T14:20:30"
}
WebSocket /ws
Sends real-time updates like:

json
Copy
Edit
{
  "event": "update",
  "data": {
    "occupied": 18,
    "available": 32
  }
}
🧪 Demo
Coming soon...

🔮 Future Enhancements
🎯 YOLOv8/YOLO-NAS based vehicle detection

📈 Add historical data dashboard with charts

📦 Save data in SQLite/PostgreSQL

🔐 Auth for admin control

📱 Mobile responsive frontend

☁️ Deploy via Docker or on cloud (e.g., AWS, Azure, GCP)

🔗 References
FastAPI Docs

WebSocket Protocol

OpenCV Documentation

YOLOv8 by Ultralytics

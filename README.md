🚗 Car Parking Space Counter
An intelligent real-time car parking space counter built using FastAPI, WebSockets, and computer vision. The system tracks available parking spots and communicates updates instantly to connected clients. Ideal for smart city infrastructure, mall parking, or campus lot monitoring.

🆕 Latest Update (📅 August 7, 2025)
Added WebSocket support to broadcast real-time parking data

Implemented /metadata endpoint to retrieve camera and system metadata (e.g. total slots, occupied slots, last updated time)

Optimized main.py for scalable socket communication with multiple clients

📁 Project Structure
graphql
Copy
Edit
parking-space-counter/
├── main.py              # FastAPI backend with WebSocket and API routes
├── detector.py          # (Optional) Parking slot detection logic
├── static/              # Frontend files (HTML/CSS/JS)
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── ...
🚀 Features
🔌 Real-time updates via WebSockets

📊 Live tracking of available and occupied parking spaces

📷 (Optional) Integration with video stream or camera feed

📡 REST API to fetch metadata and current slot status

⚙️ Scalable backend using FastAPI

📦 Installation
Clone the repository

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
Run the application

bash
Copy
Edit
uvicorn main:app --reload
🌐 API Endpoints
Method	Endpoint	Description
GET	/metadata	Returns metadata about the parking lot
WS	/ws	WebSocket endpoint for real-time updates

🔁 Sample Metadata Response
json
Copy
Edit
{
  "total_slots": 50,
  "occupied_slots": 18,
  "available_slots": 32,
  "last_updated": "2025-08-07T14:20:30"
}
📡 WebSocket Message Format
The server broadcasts JSON messages like:

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
Clients connected via JavaScript can listen and update UI accordingly.

🛠 Technologies Used
🐍 Python 3.11+

⚡ FastAPI

🌐 WebSockets

📷 OpenCV (optional, for camera integration)

🖥 HTML/CSS/JS (for frontend)

📸 Future Enhancements
AI-based vehicle detection with YOLOv8

Admin dashboard for manual overrides

Mobile app support

Database integration for historical analytics

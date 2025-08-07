import cv2
import pickle
import numpy as np
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load video and parking positions
cap = cv2.VideoCapture('carPark.mp4')
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 105, 48

# HTML route
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# WebSocket route
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for metadata in detect_and_stream_metadata():
            await websocket.send_json(metadata)
    except WebSocketDisconnect:
        print("WebSocket disconnected")

# Detection generator
async def detect_and_stream_metadata():
    global cap
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, img = cap.read()
        if not success:
            break

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThresh, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        # Occupancy check
        spaceCounter = 0
        for pos in posList:
            x, y = pos
            imgCrop = imgDilate[y:y + height, x:x + width]
            count = cv2.countNonZero(imgCrop)
            if count < 900:
                spaceCounter += 1

        total_spots = len(posList)
        metadata = {
            "frame": int(cap.get(cv2.CAP_PROP_POS_FRAMES)),
            "timestamp": datetime.now().isoformat(),
            "occupied": total_spots - spaceCounter,
            "vacant": spaceCounter,
            "total_spots": total_spots
        }

        yield metadata
        await asyncio.sleep(0.05)  # delay for streaming

    cap.release()
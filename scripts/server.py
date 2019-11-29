import asyncio
import base64
import datetime
import random

import cv2
import websockets

USERS = set()
USERDICT = {}
cap = cv2.VideoCapture(0)
async def register(websocket):
    USERS.add(websocket)
    USERDICT[websocket] = str(len(USERDICT) + 1)

async def render_webcamb(websocket):
    ret, frame = cap.read()
    ret, jpgBuffer = cv2.imencode('.jpg', frame)
    b64jpg = base64.b64encode(jpgBuffer)
    b64 = str(b64jpg)[2:-1]
    await websocket.send(b64)

async def time(websocket, path):
    await register(websocket)

    while True:
        message = "" #await websocket.recv()
        if message is not None and USERS:
            await asyncio.wait([user.send(USERDICT[websocket] + ": " + message) for user in USERS])
        await asyncio.sleep(0.25)
        await render_webcamb(websocket)



start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
import asyncio
import datetime
import random
import websockets

USERS = set()
USERDICT = {}

async def register(websocket):
    USERS.add(websocket)
    USERDICT[websocket] = str(len(USERDICT) + 1)

async def time(websocket, path):
    await register(websocket)

    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"

        message = await websocket.recv()
        if message is not None and USERS:
            await asyncio.wait([user.send(USERDICT[websocket] + ": " + message) for user in USERS])
        await asyncio.sleep(0.25)



start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
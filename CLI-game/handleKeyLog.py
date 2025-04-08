import asyncio
import websockets
import sys

async def  checkForUpdates(ws) :
    while True:
        message = await ws.recv()
        print(f"Nouveau message du serveur: {message}", file=sys.stderr)

async def sendMessages(ws) :
    try :
        while True :
            msg = input("Json to send ? (replace it with keyHandler) --> ")
            await ws.send(msg)
    except websockets.exceptions.ConnectionClosedOK:
        print("Connexion down.")
    except Exception as e:
        print(f"Unexcepted error : {e}")


async def connect_to_server():
    uri = "ws://localhost:8000/ws/game/"
    async with websockets.connect(uri) as websocket:
        task1 = asyncio.create_task(checkForUpdates(websocket))
        task2 = asyncio.create_task(sendMessages(websocket))
        await asyncio.gather(task1, task2)


asyncio.run(connect_to_server())
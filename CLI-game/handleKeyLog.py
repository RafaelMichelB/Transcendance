import sys
import requests
import inputs
import asyncio
import json
from .handleAsciiTerrain import mainPrinter

def getApiKeyCLI() : 
    res = requests.get("http://localhost:8001/get-api-key")
    if (res.status_code == 200) :
        return res.json()["api_key"]

def connectToAGame2(key : str) :
    # print("connectToAGame 1", file=sys.stderr)
    with requests.get(f"http://localhost:8001/events?apikey={key}", stream=True) as r:
        # print("connectToAGame 2", file=sys.stderr)
        for line in r.iter_lines():
            print("connectToAGame 3", file=sys.stderr)
            if line:
                dicoJsInfo = json.loads((line.decode('utf-8'))[6:])
                mainPrinter(dicoJsInfo)
                # print(type(dicoJsInfo).__name__)
                
                # print(f"Message reçu : {dicoJsInfo}", file=sys.stderr)

async def connectToAGame(key):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, connectToAGame2, key)

async def handleKeys(key : str) :
    url = f"http://localhost:8001/send-message"
    gameStarted = False
    # print("handleKeys 1", file=sys.stderr)
    while True :
        events = inputs.get_key()
        if events.ev_type == 'Key':
            if events.ev_value == 1:
                if events.ev_code == 'ESC':
                    sys.exit(0)
                if events.ev_code == 'ENTER':
                    if (gameStarted) :
                        gameStarted = False
                        requests.post(url, json={"apiKey" : key, "message" : '{"action" : "stop"}'})
                    else :
                        gameStarted = True
                        requests.post(url, json={"apiKey" : key, "message" : '{"action" : "start"}'})
                    await asyncio.sleep(1)
                if events.ev_code == 'Z':
                    requests.post(url, json={"apiKey" : key, "message" : '{"action" : "move", "player1" : "up"}'})
                if events.ev_code == 'S':
                    requests.post(url, json={"apiKey" : key, "message" : '{"action" : "move", "player1" : "down"}'})
                if events.ev_code == 'UP' :
                    requests.post(url, json={"apiKey" : key, "message" : '{"action" : "move", "player2" : "up"}'})
                if events.ev_code == 'DOWN':
                    requests.post(url, json={"apiKey" : key, "message" : '{"action" : "move", "player2" : "down"}'})

async def handleTasks(val : str) :
    task1 = asyncio.create_task(connectToAGame(val))
    # task2 = asyncio.create_task(handleKeys(val))
    await task1 # asyncio.gather(task1, task2)

val = getApiKeyCLI() # Replacewith generated output with web to link
asyncio.run(handleTasks(val))

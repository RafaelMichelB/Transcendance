import requests
import math
import asyncio
import time
import json
import sys

urlRequests = "http://django:8000/"
urlSendData = "http://rdbackend:8000/
def getActualPosition(apiKey) :
    # print(f"{urlRequests}api/simulation/?apikey={apiKey}", file=sys.stderr)
    res = requests.get(f"{urlRequests}api/simulation/?apikey={apiKey}")
    if res.status_code != 200 :
        # print(f"Error code: {res.status_code}\nData : ", file=sys.stderr)
        return
    else :
        # print(f"Data :\n{res.json()}", file=sys.stderr )
        return res.json()

def sendInfo(apiKey) :
    try :
        position = getActualInfo(apiKey)
        while position["team1Score"] < 5 and position["team2Score"] < 5 :
            racketY = position["Player2"]
            for _ in range(20) :
                posYAi = racketY[1][1] - racketY[0][1]
                resultStats = posYAi - position["ball"]["position"][1]
                if resultStats < -5 :
                    requests.post(f"{urlSendData}/send-message", json={"apiKey": apiKey, "message": '{"action": "move", "player2": "up"}'})
                elif resultStats > 5 :
                    requests.post(f"{urlSendData}/send-message", json={"apiKey": apiKey, "message": '{"action": "move", "player2": "down"}'})
                time.sleep(0.05)
    except Exception as e:
        pass

getActualPosition("17c3015f-fb62-450d-bdf9-9bc54f41bdf1")

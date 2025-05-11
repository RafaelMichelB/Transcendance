from django.shortcuts import render
import requests
from django.http import HttpResponse
import math
import asyncio
import time
import json
import sys
import threading
from http import HTTPStatus

urlRequests = "http://django:8000/"

class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

loopAi = asyncio.new_event_loop()
threading.Thread(target=start_loop, args=(loopAi,), daemon=True).start()

async def getActualPosition(apiKey) :
    # print(f"{urlRequests}api/simulation/?apikey={apiKey}", file=sys.stderr)
    try :
        print("sendInfo 11", file=sys.stderr)
        res = requests.get(f"{urlRequests}api/simulation?apikey={apiKey}")
        print("sendInfo 12", file=sys.stderr)
        if res.status_code != 200 :
            print(f"Error code: {res.status_code}\nData : ", file=sys.stderr)
            return
        else :
            print(f"It worked : {res.json()}")
            return res.json()
    except Exception as e :
        print(f"error getActualPos : {e}", file=sys.stderr)

async def sendInfo(apiKey) :
    try :
        asyncio.sleep(0.5)
        print("sendInfo 1", file=sys.stderr)
        position = await getActualPosition(apiKey)
        print("sendInfo 2", file=sys.stderr)
        while position["team1Score"] < 5 and position["team2Score"] < 5 :
            print("sendInfo 3", file=sys.stderr)
            racketY = position["player2"]
            for j in range(20) :
                posYAi = (racketY[1][1] + racketY[0][1]) / 2
                resultStats = posYAi - position["ball"]["position"][1]
                print(f"racketY : {racketY}", file=sys.stderr)
                print(f"sendInfo 4 {j}", file=sys.stderr)
                print(f'ball POs : {position["ball"]["position"][1]}', file=sys.stderr)
                print(f"posYai : {posYAi}", file=sys.stderr)
                print(f"resultStat {j} : {resultStats}", file=sys.stderr)
                if resultStats < -5 :
                    requests.post(f"{urlRequests}/send-message", json={"apiKey": apiKey, "message": '{"action": "move", "player2": "down"}'})
                    racketY[0][1] -= 5
                    racketY[1][1] -= 5 
                elif resultStats > 5 :
                    requests.post(f"{urlRequests}/send-message", json={"apiKey": apiKey, "message": '{"action": "move", "player2": "up"}'})
                    racketY[0][1] += 5
                    racketY[1][1] += 5
                time.sleep(0.05)
            position = await getActualPosition(apiKey)
            print(f"position : {position}", file=sys.stderr)
    except Exception as e:
        print(f"error : {e}", file=sys.stderr)
        pass

def initAI(request) :
    apikey = request.GET.get('apikey', "None")
    asyncio.run_coroutine_threadsafe(sendInfo(apikey), loopAi)
    return HttpResponseNoContent()
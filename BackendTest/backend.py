from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import uuid
from channels_redis.core import RedisChannelLayer
from asgiref.sync import async_to_sync
import websockets
import asyncio
import sys
import json
import time

dictActivePlayer = {}
apiKeysUnplayable = []
dictApi = {}
dictApiSp = {}
apiKeys = []
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet à toutes les origines d'accéder
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les headers
)

channel_layer = RedisChannelLayer(
    hosts=[("redis", 6379)]  # ou l’URL de ton Redis
)

uri = "ws://django:8000/ws/game/"


class   RequestParsed :
    def __init__(self, apiKey, action) :
        if apiKey in apiKeys or apiKey in apiKeysUnplayable :
            self.apiKey = apiKey
        else :
            self.apiKey = None
        self.action = action


from datetime import datetime
async def  checkForUpdates(uriKey, key) :
    try :
        async with websockets.connect(uriKey) as ws:
            while True:
                # Attendre la réception d'un message depuis le WebSocket
                message = await ws.recv() #asyncio.wait_for(ws.recv(), timeout=10) #await ws.recv  # Attend le message venant du WebSocket
                print(f"Ws : {ws}, uriKey : {uriKey} <-> message : {message}", file=sys.stderr)
                # Formater l'événement SSE (Server-Sent Event)
                yield f"data: {message}\n\n"

        print("[Debug BACKEND checkForUpdate()] - Websocket Closed", file=sys.stderr)
#    except asyncio.TimeoutError :       
    except Exception as e :
        print(f"[checkForUpdates] WebSocket {ws}  error : {e}", file=sys.stderr)
        yield f"data: WebSocket stop\n\n"



@app.get("/events")
async def sse(request: Request, apikey: str = None, idplayer=None):
    rq = RequestParsed(apikey, {})
    if (rq.apiKey) :
        return StreamingResponse(checkForUpdates(f"{uri}?room={rq.apiKey}&userid={idplayer}", rq.apiKey), media_type="text/event-stream")

@app.post("/set-api-key-alone")
def setApiKeySp(request: Request, apikey:str=None):
    print(apikey, file=sys.stderr)
    dictApiSp[apikey] = 1
    apiKeys.append(apikey)
    return JSONResponse(content={"playable": "Game can start"})

@app.post("/set-api-key")
def setApiKey(request: Request, apikey:str=None):
    print(apikey, file=sys.stderr)
    if apikey not in apiKeysUnplayable:
        return JSONResponse(content={"playable" : f"Room {apikey} doesn't Exists"})
    if apikey in dictApi :
        dictApi[apikey] += 1
    else :
        dictApi[apikey] = 1

    if (dictApi[apikey] > 1) :
        apiKeysUnplayable.remove(apikey)
        apiKeys.append(apikey)
        playable = "Game can start"
    else :
        playable = "Need more player"

    return JSONResponse(content={"playable": playable})

@app.get("/get-api-key")
def get_api_key():
    api_key = str(uuid.uuid4())

    apiKeysUnplayable.append(api_key)

    return JSONResponse(content={"api_key": api_key})

@app.post("/is-game-playable")
def isGamePlayable(request: Request, apikey=None) :
    if (dictApi[apikey] > 1) :
        apiKeys.append(apikey)
        playable = "Game can start"
    else :
        playable = "Need more player"
    print(f"playable : {playable}", file=sys.stderr)
    return JSONResponse(content={"playable": playable})


@app.post("/send-message")
async def sendNewJSON(request: Request):
    raw_body = await request.body()
    decoded = raw_body.decode("utf-8")

    dictionnaryJson = json.loads(decoded)
    # print(f"dictio : {dictionnaryJson}")
    rq = RequestParsed(dictionnaryJson.get("apiKey", None), dictionnaryJson.get("message", {}))
    # print(rq.apiKey, file=sys.stderr)
    if (rq.apiKey) :
        # print(f"Heyo : {type(rq.action).__name__} | {rq.action}", file=sys.stderr)
        await channel_layer.group_send(
            rq.apiKey,
            {
                "type": "tempReceived",
                "text_data": rq.action
            }
        )
    # print(f"Reiceived Json : {dictionnaryJson}", file=sys.stderr)

@app.get("/leave-game")
async def disconnectUser(request:Request, apikey, idplayer) :
    rq = RequestParsed(apikey, {})
    if (rq.apiKey) :
        await channel_layer.group_send(
            rq.apiKey,
            {
                "type" : "tempReceived",
                "text_data" : f'{{"action" : "forfait", "player" : {idplayer}}}'
            }
        )
        print("discoUsr1", file=sys.stderr)
        try :
            dictApi.pop(rq.apiKey)
        except KeyError:
            try :
                dictApiSp.pop(rq.apiKey)
            except KeyError:
                return
        try :
            apiKeys.remove(apikey)
        except Exception:
            apiKeysUnplayable.remove(apikey)


#async def stopGameForfait(




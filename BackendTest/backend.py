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
        if apiKey in apiKeys :
            self.apiKey = apiKey
        else :
            self.apiKey = None
        self.action = action


async def  checkForUpdates(uriKey) :
    try :
        async with websockets.connect(uriKey) as ws:
            while True:
                # Attendre la réception d'un message depuis le WebSocket
                message = await ws.recv()  # Attend le message venant du WebSocket
                # Formater l'événement SSE (Server-Sent Event)
                yield f"data: {message}\n\n"
    except Exception as e :
        # print(f"[checkForUpdates] WebSocket error : {e}", file=sys.stderr)
        yield f"data: WebSocket stop\n\n"



@app.get("/events")
async def sse(request: Request, apikey: str = None):
    rq = RequestParsed(apikey, {})
    if (rq.apiKey) :
        return StreamingResponse(checkForUpdates(f"{uri}?room={rq.apiKey}"), media_type="text/event-stream")


@app.get("/get-api-key")
def get_api_key():
    api_key = str(uuid.uuid4())

    apiKeys.append(api_key)

    return JSONResponse(content={"api_key": api_key})

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




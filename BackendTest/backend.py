from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import uuid
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

uri = "ws://django:8000/ws/game/"


class   RequestParsed :
    def __init__(self, apiKey, action) :
        if apiKey in apiKeys :
            self.apiKey = apiKey
        else :
            self.apiKey = None
        self.action = action


async def  checkForUpdates(uriKey) :
    async with websockets.connect(uriKey) as ws:
        while True:
            # Attendre la réception d'un message depuis le WebSocket
            message = await ws.recv()  # Attend le message venant du WebSocket
            # Formater l'événement SSE (Server-Sent Event)
            yield f"data: {message}\n\n"

@app.get("/events")
async def sse(request: Request, apikey: str = None):
    print("1", file=sys.stderr)
    rq = RequestParsed(apikey, {})
    print("5", file=sys.stderr)
    if (rq.apiKey) :
        print("6", file=sys.stderr)
        return StreamingResponse(checkForUpdates(f"{uri}?room={rq.apiKey}"), media_type="text/event-stream")


@app.get("/get-api-key")
def get_api_key():
    api_key = str(uuid.uuid4())

    apiKeys.append(api_key)

    return JSONResponse(content={"api_key": api_key})

@app.post("/send-new-data")
async def sendNewJSON(request: Request):
    raw_body = await request.body()
    decoded = raw_body.decode("utf-8")

    dictionnaryJson = json.loads()
    rq = RequestParsed(dictionnaryJson.get("apiKey", None), dictionnaryJson.get("actionDic", {}))
    if (rq.apiKey) :
        async_to_sync(channel_layer.group_send)(
            rq.apiKey,
            {
                "type": "tempReceived",
                "text_data": json.dumps(rq.action)
            }
        )
    print(f"Reiceived Json : {dictionnaryJson}", file=sys.stderr)




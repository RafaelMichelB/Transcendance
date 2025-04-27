import requests
import math
import asyncio
import time
import json
import sys

urlRequests = "http://django:8000/"
urlSendData = "http://rdbackend:8000/
def getActualPosition(apiKey) :
    while True :
        asyncio.sleep(1)
        print(f"{urlRequests}api/simulation/?apikey={apiKey}", file=sys.stderr)
        res = requests.get(f"{urlRequests}api/simulation/?apikey={apiKey}")
        if res.status_code != 200 :
            print(f"Error code: {res.status_code}\nData : ", file=sys.stderr)
            return
        else :
            print(f"Data :\n{res.json()}", file=sys.stderr )

def 


getActualPosition("17c3015f-fb62-450d-bdf9-9bc54f41bdf1")

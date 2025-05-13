from pynput import keyboard
import asyncio
import sys
import requests

pressed_keys = set()
stop_event = asyncio.Event()

def on_press(key):
    pressed_keys.add(key)

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)
    try :
        if key.char == 'q':
            stop_event.set()
            return False  # Stop listener
    except AttributeError :
        pass

async def is_pressed(url_post, val):
    started = False
    while not stop_event.is_set():
        # #print(handler)
        if pressed_keys:
            names = []
            for k in pressed_keys:
                try:
                    names.append(k.char)
                except AttributeError:
                    names.append(str(k))
            if "Key.up" in names :
                requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player2": "up"}'})
            elif "Key.down" in names:
                requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player2": "down"}'})
            if ('w' in names) :
                requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player1": "up"}'})
            elif 's' in names :
                requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player1": "down"}'})
            elif 'p' in names:
                if not started:
                    started = True
                    requests.post(url_post, json={"apiKey": val, "message": f'{{"action": "start"}}'})
        await asyncio.sleep(0.05)

async def mainKeyHandler(url:str, apiKey:str):
    loop = asyncio.get_event_loop()
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    await is_pressed(url, apiKey)

# asyncio.run(mainKeyHandler("Hello"))

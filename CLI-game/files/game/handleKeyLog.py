import sys
import requests
import json
import curses
import select
import threading
import time
import traceback
from .handleAsciiTerrain import mainPrinter
import pynput
import asyncio
from .keyPressed import mainKeyHandler

adress = "10.13.5.5"


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

loopKeyHandler = asyncio.new_event_loop()
threading.Thread(target=start_loop, args=(loopKeyHandler,), daemon=True).start()

def getApiKeyCLI() :
    res = requests.get(f"http://{adress}:8001/get-api-key")
    if (res.status_code == 200) :
        return res.json()["api_key"]

def setApiKeyCLI(apikey) :
    res = requests.post(f"http://{adress}:8001/set-api-key?apikey={apikey}")
    if (res.status_code == 200) :
        return res.json()["playable"]
    else :
        return f"Unknown Error : {res.status_code}"

def setApiKeySpCLI(apikey) :
    res = requests.post(f"http://{adress}:8001/set-api-key-alone?apikey={apikey}")
    if (res.status_code == 200) :
        return res.json()["playable"]
    else :
        return f"Unknown Error : {res.status_code}"

def loadGamePlayable(apikey) :
    res = requests.post(f"http://{adress}:8001/is-game-playable?apikey={apikey}")
    if (res.status_code == 200) :
        return res.json()["playable"]
    else :
        return f"Unknown Error : {res.status_code}"


def handleGame(stdscr, val, nP1, nP2) :
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.clear()

    url_sse = f"http://{adress}:8001/events?apikey={val}&idplayer=0"
    url_post = f"http://{adress}:8001/send-message"
    url_leave = f"http://{adress}:8001/leave-game?apikey={val}"
    started = False

    with requests.get(url_sse, stream=True) as r:
        lines = r.iter_lines()
        sock = r.raw._fp.fp

        asyncio.run_coroutine_threadsafe(mainKeyHandler(url_post, val), loopKeyHandler)

        buffer = ""
        last_update = ""
        scoresString = f"{nP1} : 0                 ||                 {nP2} : 0\n"
        stdscr.addstr(0, 0, f"{nP1}, press ↑ ↓ to move / {nP2}, press w s to move, p to start, q to quit.")

        while True:
            # requests.get(f"http://{adress}:8001/debug")

            key = stdscr.getch()
            if (key == ord('q')) : 
                requests.get(url_leave)
                break
            ready, _, _ = select.select([sock], [], [], 0.01)
            if ready:
                try:
                    line = next(lines).decode("utf-8")
                    if line.startswith("data: "):
                        if (len(line) > 6) :
                            content = line[6:]
                        else :
                            content = "{wwwd}"
                        try:
                            dico = json.loads(content)
                            last_update = mainPrinter(dico)
                            scoresString = f"{nP1} : {dico['game_stats']['team1Score']}                 ||                 {nP2} : {dico['game_stats']['team2Score']}\n"
                        except Exception as e:
                            pass
                except StopIteration:
                    break
                except Exception as e:
                    last_update = f"[Erreur SSE] {str(e)}"

            stdscr.addstr(2, 0, f"game State :\n{last_update}\n\nScores : {scoresString}")
            stdscr.refresh()

            time.sleep(0.01)


def handleGame2Players(stdscr, val, playerID) :
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    stdscr.clear()
    url_sse = f"http://{adress}:8001/events?apikey={val}&idplayer={playerID}"
    url_post = f"http://{adress}:8001/send-message"
    url_leave = f"http://{adress}:8001/leave-game?apikey={val}"
    started = False

    with requests.get(url_sse, stream=True) as r:
        lines = r.iter_lines()
        sock = r.raw._fp.fp

        buffer = ""
        last_update = ""
        scoresString = f"{1} : 0                 ||                 {2} : 0\n"
        stdscr.addstr(0, 0, f"{1}, press ↑ ↓ to move / {2}, press w s to move, p to start, q to quit.")

        while True:
            key = stdscr.getch()
            if key != -1:
                if key == curses.KEY_UP:
                    if playerID == 2 :
                        requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player2": "up"}'})
                    else :
                        requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player1": "up"}'})

                elif key == curses.KEY_DOWN:
                    if playerID == 2 :
                        requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player2": "down"}'})
                    else :
                        requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player1": "down"}'})
                elif key == ord('p') and playerID == 1:
                    if not started:
                        started = True
                        requests.post(url_post, json={"apiKey": val, "message": f'{{"action": "start"}}'})
                elif key == ord('q'):
                    requests.get(url_leave)
                    break


            ready, _, _ = select.select([sock], [], [], 0.01)
            if ready:
                try:
                    line = next(lines).decode("utf-8")
                    if line.startswith("data: "):
                        if (len(line) > 6) :
                            content = line[6:]
                        else :
                            content = "{wwwd}"
                        try:
                            dico = json.loads(content)
                            last_update = mainPrinter(dico)
                            scoresString = f"{1} : {dico['game_stats']['team1Score']}                 ||                 {2} : {dico['game_stats']['team2Score']}\n"
                        except Exception as e:
                            pass
                except StopIteration:
                    break
                except Exception as e:
                    last_update = f"[Erreur SSE] {str(e)}"

            stdscr.addstr(2, 0, f"game State :\n{last_update}\n\nScores : {scoresString}")
            stdscr.refresh()

            time.sleep(0.01)

def inputField(stdscr, y, x, prompt, maxL, defaultChar=' '):
    stdscr.addstr(y, x, prompt)
    curses.curs_set(1)
    curses.noecho()

    buffer = ""
    while True:
        key = stdscr.getch()
        if key in (curses.KEY_ENTER, 10, 13):
            break
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if buffer:
                buffer = buffer[:-1]
                stdscr.move(y, x + len(prompt) + len(buffer))
                stdscr.addch(defaultChar)
                stdscr.move(y, x + len(prompt) + len(buffer))
        elif (32 <= key <= 126) and len(buffer) < maxL:
            buffer += chr(key)
            stdscr.addstr(y, x + len(prompt) + len(buffer) - 1, chr(key))

        stdscr.refresh()

    curses.curs_set(0)
    return buffer

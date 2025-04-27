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

adress = "127.0.0.1"
lstFuncFront=[]
lstFuncBack=[]

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

loopKeyHandler = asyncio.new_event_loop()
threading.Thread(target=start_loop, args=(loopKeyHandler,), daemon=True).start()

def addFunc(name) :
    lstFuncFront.append(name)

def handleClassicFuncMove(dictionnary, oldFuncName, newFuncName, stdscr, classScreen) :
    lstFuncBack.append(oldFuncName)
    return dictionnary[newFuncName](stdscr, classScreen)

def handleBackward(funcName, dictFunctionsAllowed, apiKey, stdscr, classScreen):
    # if (apiKey != None) :
    #     print("Yike")
    #     leaveGameCLI(apiKey)
    lstFuncFront.append(funcName)
    args = (stdscr, classScreen)
    if (len(lstFuncBack) > 0) :
        return dictFunctionsAllowed[lstFuncBack.pop(-1)](*args)
    return

def handleForward(funcName, dictFunctionsAllowed, apiKey, stdscr, classScreen) :
    try :
        nextFunc = lstFuncFront.pop(-1)
        lstFuncBack.append(funcName)
        args = (stdscr, classScreen)
        return dictFunctionsAllowed[nextFunc](*args)
    except Exception :
        return

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

def leaveGameCLI(apiKey) :
    res=requests.get(f"http://{adress}:8001/leave-game?apikey={apiKey}&idplayer=0")

def handleGame(stdscr, val, nP1, nP2) :
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.clear()

    url_sse = f"http://{adress}:8001/events?apikey={val}&idplayer=0"
    url_post = f"http://{adress}:8001/send-message"
    url_leave = f"http://{adress}:8001/leave-game?apikey={val}&idplayer=0"
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
            key = stdscr.getch()
            if (key == ord('q')) : 
                return leaveGameCLI(val)
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
                            last_update = mainPrinter(dico, stdscr, val)
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

def handleResult(stdscr, apikey, playerID) :
    stringResult = """+------------------------------------------------------------------------------------+
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                Match Finished                                      |
|                                                                                    |
|                                                                                    |
|                                   You                                              |
|                                                                                    |
|                                                                                    |
|              press L to back tolobby                                               |
|              press Q to quit program                                               |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
+------------------------------------------------------------------------------------+"""
    curses.endwin()
    input(stringResult)
    stdscr.refresh()
    res=requests.get(f"http://{adress}:8001/leave-game?apikey={apikey}&idplayer={playerID}")
    stdscr.addstr(2, 0, stringResult)
    if dictionnaryResult["Winning"] :
        stdscr.addstr(10, 41, f'Won |-> {dictionnaryResult["finalScore"]["Player1"]} / {dictionnaryResult["finalScore"]["Player2"]} <-|')
        stdscr.refresh()
        while True :
            key = stdscr.getch()
            if key == ord('l') :
                return sendLobby(stdscr)
            elif key == ord('q') :
                return


def handleGame2Players(stdscr, val, playerID) :
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    stdscr.clear()
    url_sse = f"http://{adress}:8001/events?apikey={val}&idplayer={playerID}"
    url_post = f"http://{adress}:8001/send-message"
    url_leave = f"http://{adress}:8001/leave-game?apikey={val}&idplayer={playerID}"
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
                    return handleResult(stdscr, val, playerID)


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
                            last_update = mainPrinter(dico, stdscr)
                            scoresString = f"{1} : {dico['game_stats']['team1Score']}                 ||                 {2} : {dico['game_stats']['team2Score']}\n"
                        except Exception as e:
                            pass
                except StopIteration:
                    break
                except Exception as e:
                    last_update = f"[Erreur SSE] {str(e)}"
            # curses.endwin()
            # input(last_update)
            # stdscr.refresh()
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



import sys
import requests
import threading
import json
import curses
import select
import time
from .handleAsciiTerrain import mainPrinter

def getApiKeyCLI() : 
    res = requests.get("http://rdbackend:8000/get-api-key")
    if (res.status_code == 200) :
        return res.json()["api_key"]

val = getApiKeyCLI() # Replacewith generated output with web to link


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    url_sse = f"http://rdbackend:8000/events?apikey={val}"
    url_post = "http://rdbackend:8000/send-message"
    started = False

    with requests.get(url_sse, stream=True) as r:
        lines = r.iter_lines()
        sock = r.raw._fp.fp

        buffer = ""
        last_update = ""
        scoresString = "Player1 : 0                 ||                 Player2 : 0\n"

        while True:
            key = stdscr.getch()
            if key != -1:
                if key == curses.KEY_UP:
                    requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player2": "up"}'})
                elif key == curses.KEY_DOWN:
                    requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player2": "down"}'})
                elif key == ord('w'):
                    requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player1": "up"}'})
                elif key == ord('s'):
                    requests.post(url_post, json={"apiKey": val, "message": '{"action": "move", "player1": "down"}'})
                elif key == ord('p'):
                    action = "start" if not started else "stop"
                    started = not started
                    requests.post(url_post, json={"apiKey": val, "message": f'{{"action": "{action}"}}'})
                elif key == ord('q'):
                    break

            ready, _, _ = select.select([sock], [], [], 0.01)
            if ready:
                try:
                    line = next(lines).decode("utf-8")
                    if line.startswith("data: "):
                        content = line[6:]
                        try:
                            dico = json.loads(content)
                            last_update = mainPrinter(dico)
                            scoresString = f"Player1 : {dico['game_stats']['team1Score']}                 ||                 Player2 : {dico['game_stats']['team2Score']}\n"
                        except Exception:
                            pass
                except StopIteration:
                    break
                except Exception as e:
                    last_update = f"[Erreur SSE] {str(e)}"

            stdscr.clear()
            stdscr.addstr(0, 0, "Appuie sur ↑ ↓ / w s pour bouger, p pour start/stop, q pour quitter.")
            stdscr.addstr(2, 0, f"Dernier état :\n{last_update}\n\nScores : {scoresString}")
            stdscr.refresh()

            time.sleep(0.01)

curses.wrapper(main)

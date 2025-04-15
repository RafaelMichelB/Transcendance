import curses
import time

def message_stream():
    for i in range(20):
        yield f"Message n°{i}"
        time.sleep(0.5)

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(False)  # getch() bloquant si besoin
    curses.noecho()

    line = 1  # Position Y d'affichage
    for msg in message_stream():
        stdscr.addstr(line, 0, msg)
        stdscr.refresh()
        # line += 1

        if line > curses.LINES - 2:
            stdscr.clear()
            line = 1

    stdscr.addstr(line + 2, 2, "Terminé ! Appuie sur une touche pour quitter.")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)

# import curses

# def main(stdscr):
#     # Initialisation
#     curses.curs_set(0)         # Cache le curseur
#     stdscr.nodelay(True)       # getch() non bloquant
#     stdscr.keypad(True)        # Permet les touches spéciales (flèches)
#     curses.noecho()            # Ne pas afficher les touches
#     curses.cbreak()            # Mode "caractère par caractère"

#     y, x = 5, 10               # Position de départ
#     max_y, max_x = stdscr.getmaxyx()

#     while True:
#         stdscr.clear()
#         stdscr.addstr(0, 0, "Utilise les flèches pour déplacer. Appuie sur 'q' pour quitter.")
#         stdscr.addstr(y, x, "[]")  # Le "joueur"

#         key = stdscr.getch()

#         if key == ord('q'):
#             break
#         elif key == curses.KEY_UP and y > 1:
#             y -= 1
#         elif key == curses.KEY_DOWN and y < max_y - 2:
#             y += 1
#         elif key == curses.KEY_LEFT and x > 1:
#             x -= 1
#         elif key == curses.KEY_RIGHT and x < max_x - 3:
#             x += 1

#         stdscr.refresh()
#         curses.napms(50)  # Petit délai pour éviter de tourner trop vite

# curses.wrapper(main)

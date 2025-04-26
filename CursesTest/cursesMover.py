from pynput import keyboard
import asyncio
import sys
import curses


def main(stdscr) :
    while True:
        key = stdscr.getch()
        print(str(key))


curses.wrapper(main)




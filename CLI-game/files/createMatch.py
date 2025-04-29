from .dataScreens import Screen, loadInfo
import time
import curses
from .game.handleKeyLog import getApiKeyCLI, setApiKeyCLI, loadGamePlayable, handleGame, setApiKeySpCLI, inputField, handleGame2Players, handleClassicFuncMove, handleBackward, handleForward, addFunc
import sys

val = "0000" #getApiKeyCLI() # Replacewith generated output with web to link

dictGameMode = {'1' : "Join regular game", '2' : "Create regular game", '3' : "Join tournament", '4' : "Create tournament", '5' : "Create Local game ", '6' : "Create game versus AI"}

def sendGameCreation(stdscr, classScreen, dictFunctionsAllowed, apiKey=None) :
    apiKey = getApiKeyCLI()
    infogameCreation = classScreen.getSpecificInfo("RoomClassicCreate")
    isGamePlayable = setApiKeyCLI(apiKey)
    stdscr.addstr(2, 0, loadInfo(infogameCreation))
    stdscr.addstr(1 + infogameCreation["outputPos"][0], infogameCreation["outputPos"][1], apiKey)
    while True :
        isGamePlayable = loadGamePlayable(apiKey)
        stdscr.addstr(1 + infogameCreation["inputPos"][0], 0, "|                          Game state :                                              |")
        stdscr.addstr(1 + infogameCreation["inputPos"][0], infogameCreation["inputPos"][1], isGamePlayable)
        stdscr.refresh()
        if (isGamePlayable == "Game can start") :
            time.sleep(0.5)
            return handleGame2Players(stdscr, apiKey, 1, dictFunctionsAllowed)
        stdscr.nodelay(True)
        key = stdscr.getch()
        if (key == 260) :
            stdscr.nodelay(False)
            return handleBackward("sendGameCreation", dictFunctionsAllowed, apiKey, stdscr, classScreen) 
        if (key == 261) :
            stdscr.nodelay(False)
            return handleForward("sendGameCreation", dictFunctionsAllowed, apiKey, stdscr, classScreen)
        stdscr.nodelay(False)
        time.sleep(0.3)


def sendGameJoining(stdscr, classScreen, dictFunctionsAllowed, apiKey=None) :
    infoGameJoining = classScreen.getSpecificInfo("RoomClassicJoin")
    stdscr.addstr(2, 0, loadInfo(infoGameJoining))
    isRoomAvalaible = False
    while not isRoomAvalaible :
        stdscr.nodelay(True)
        key = stdscr.getch()
        if key == 260 :
            return handleBackward("sendGameJoining", dictFunctionsAllowed, apiKey, stdscr, classScreen)
        if (key == 261) :
            return handleForward("sendGameJoining", dictFunctionsAllowed, apiKey, stdscr, classScreen)
        stdscr.refresh()
        inputGameID = inputField(stdscr, 1 + infoGameJoining["inputPos"][0], infoGameJoining["inputPos"][1], "", 40) # stdscr.getstr(1 + infoGameJoining["inputPos"][0], infoGameJoining["inputPos"][1]).decode('utf-8')
        isGamePlayable = setApiKeyCLI(inputGameID)
        stdscr.addstr(1 + infoGameJoining["outputPos"][0], 0, "|          |                                                               |         |")
        stdscr.addstr(1 + infoGameJoining["outputPos"][0], infoGameJoining["outputPos"][1], isGamePlayable)
        stdscr.refresh()
        if isGamePlayable != f"Room {inputGameID} doesn't Exists" :
            isRoomAvalaible = True
    while True :
        isGamePlayable = loadGamePlayable(inputGameID)
        stdscr.addstr(1 + infoGameJoining["outputPos"][0], 0, "|          |                                                               |         |")
        stdscr.addstr(1 + infoGameJoining["outputPos"][0], infoGameJoining["outputPos"][1], isGamePlayable)
        stdscr.refresh()
        if (isGamePlayable == "Game can start") :
            time.sleep(0.5)
            addFunc('sendGameJoining')
            return handleGame2Players(stdscr, inputGameID, 2, dictFunctionsAllowed)
        time.sleep(0.3)

def sendLocalGame(stdscr, classScreen, dictFunctionsAllowed, apiKey=None) :
    infoSinglePlayer = classScreen.getSpecificInfo("SinglePlayer")
    stdscr.addstr(2, 0, loadInfo(infoSinglePlayer))
    stdscr.refresh()
    namePlayer1 = inputField(stdscr, 1 + infoSinglePlayer["inputPos"][0], infoSinglePlayer["inputPos"][1], "NameP1: ", 10)
    namePlayer2 = inputField(stdscr, 1 + infoSinglePlayer["outputPos"][0], infoSinglePlayer["outputPos"][1], "NameP2: ", 10)
    key = getApiKeyCLI()
    setApiKeySpCLI(key)
    handleGame(stdscr, key, namePlayer1, namePlayer2, dictFunctionsAllowed)


def sendLobby(stdscr, classScreen=Screen(), dictFunctionsAllowed=None, apiKey=None) :
    infoLobby = classScreen.getSpecificInfo("Lobby")
    screenLobby = loadInfo(infoLobby)
    stdscr.addstr(2, 0, screenLobby)
    stdscr.refresh()
    while True :
        key = stdscr.getch()
        if key != -1 :
            if (key == 260) :
                return handleBackward("sendLobby", dictFunctionsAllowed, apiKey, stdscr,classScreen)
            if (key == 261) :
                return handleForward("sendLobby", dictFunctionsAllowed, apiKey, stdscr, classScreen)
            stdscr.addstr(16, 0, "|                      Which game mode ? : ____________________                      |")
            stdscr.addstr(1 + infoLobby["inputPos"][0], infoLobby["inputPos"][1], dictGameMode.get(chr(key), "Unknown input"))
            stdscr.refresh()
            time.sleep(0.5)
            if key == ord('1') :
                return handleClassicFuncMove(dictFunctionsAllowed, "sendLobby", "sendGameJoining", stdscr,classScreen)
            elif key == ord('2') :
                return handleClassicFuncMove(dictFunctionsAllowed,"sendLobby", "sendGameCreation", stdscr, classScreen)
            elif key == ord('3') :
                pass
            elif key == ord('4') :
                pass
            elif key == ord('5') :
                return handleClassicFuncMove(dictFunctionsAllowed, "sendLobby", "sendLocalGame", stdscr, classScreen)

dictFunctionsAllowed = {
        "sendLobby" : sendLobby,
        "sendLocalGame" : sendLocalGame,
        "sendGameJoining" : sendGameJoining,
        "sendGameCreation" : sendGameCreation
}

def main(stdscr):
    print("Hello world", file=sys.stderr)
    screens = Screen()
    return sendLobby(stdscr, screens, dictFunctionsAllowed)

curses.wrapper(main)

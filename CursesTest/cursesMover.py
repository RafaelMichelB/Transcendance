from pynput import keyboard
import asyncio
import sys

pressed_keys = set()
stop_event = asyncio.Event()

def on_press(key):
    pressed_keys.add(key)

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)
    if key == keyboard.Key.esc:
        print("Escape ressed, stopping listener.", file=sys.stderr)
        # handler = False
        stop_event.set()
        # print("hand: ", handler)
        return False  # Stop listener

async def is_pressed():
    while not stop_event.is_set():
        # print(handler)
        if pressed_keys:
            names = []
            for k in pressed_keys:
                try:
                    names.append(k.char)
                except AttributeError:
                    names.append(str(k))
            print(f"Touchez pressées : {', '.join(names)}")
        else:
            print("Aucune touche", file=sys.stderr)
        await asyncio.sleep(0.5)

async def main():
    loop = asyncio.get_event_loop()
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # Non-bloquant
    await is_pressed()  # Lancer ta boucle d'affichage

asyncio.run(main())

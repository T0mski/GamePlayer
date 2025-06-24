import pyautogui as gui
import time
from pynput import keyboard as kb
import threading as th

running = True
def quit():
    return False

def Update():
    mousePos = gui.position()
    time.sleep(0.5)
    print(mousePos)

def listen_for_exit():
    def on_press(key):
        global running
        if key == kb.Key.esc:
            print("Escape pressed. Stopping...")
            running = False
            return False


    with kb.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    listenerThread = th.Thread(target=listen_for_exit)
    listenerThread.start()

    while running:
        Update()
        time.sleep(0.2)
    print("Program Exited")
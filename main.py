import pyautogui as gui
import time
from pynput import keyboard as kb
import threading as th
from GUI import GameOverlay
import tkinter as tk


running = True
TopLeft = ()
BottomRight = ()
Parameters = {
    "TopLeft": (),
    "BottomRight": (),
    "Width": 0,
    "Height": 0
}

def Update():
    time.sleep(0.5)

def listener():
    def on_press(key):
        global running
        global pressed
        global Parameters
        if key == kb.Key.esc:
            print("Escape pressed. Stopping...")
            running = False
            return False
        if key == kb.Key.ctrl_l:
            print("Storing first")
            Parameters["TopLeft"] = gui.position()

        if key == kb.Key.alt_l:
            print("Storing second")
            Parameters["BottomRight"] = gui.position()
        if key == kb.Key.enter:
            TopLeft = Parameters["TopLeft"]
            BottomRight = Parameters["BottomRight"]
            width = BottomRight.x - TopLeft.x
            Parameters["Width"] = width
            height = BottomRight.y - TopLeft.y
            Parameters["Height"] = height
            print("Calculating...")
            print(f"Width: {width} Height: {height}")

    with kb.Listener(on_press=on_press) as listener:
        listener.join()




def loadWidget():
    def createWindow():
        root = tk.Tk()
        app = GameOverlay(root)
        root.mainloop()


    createWindow()

if __name__ == "__main__":
    listenerThread = th.Thread(target=listener, daemon=True)
    listenerThread.start()
    windowThread = th.Thread(target=loadWidget, daemon=True)
    windowThread.start()
    while running:
        Update()
    print("Program Exited")
    print(f"Top-Left Coords: {Parameters["TopLeft"]}, Bottom-Right Coords: {Parameters["BottomRight"]}")

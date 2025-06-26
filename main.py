# Importing Libraries.
import pyautogui as gui
import os
import time
from mouseinfo import screenshot
from pynput import keyboard as kb
import threading as th
from GUI import GameOverlay
import tkinter as tk
import mss
import mss.tools
from PIL import Image
import numpy as np

# Declaring Global Variables.
running = True
TopLeft = ()
BottomRight = ()
Parameters = {
    "TopLeft": (),
    "BottomRight": (),
    "Width": 0.0,
    "Height": 0.0,
    "Calculated": False

}

# Update function that allows the Program to run constanly.
def Update():
    captureWindow()
    time.sleep(0.5)


# function that is called on the Keyboard Listener Thread of the program.
def listener_Thread():
    def on_press(key):
        global running
        global pressed
        global Parameters
        if key == kb.Key.esc:
            print("Escape pressed. Stopping...")
            running = False
            return False
        if key == kb.Key.ctrl_l:
            print("Storing TopLeft")
            Parameters["TopLeft"] = gui.position()
        if key == kb.Key.alt_l:
            print("Storing BottomRight")
            Parameters["BottomRight"] = gui.position()
        if key == kb.Key.enter:
            TopLeft = Parameters["TopLeft"]
            BottomRight = Parameters["BottomRight"]
            width = BottomRight.x - TopLeft.x
            Parameters["Width"] = width
            height = BottomRight.y - TopLeft.y
            Parameters["Height"] = height
            Parameters["Calculated"] = True
            print("Calculating...")
    with kb.Listener(on_press=on_press) as listener:
        listener.join()



# function that is called on the Load widget Thread of the program.
def loadWidget_Thread():
    def createWindow():
        root = tk.Tk()
        app = GameOverlay(root)
        root.mainloop()


    createWindow()

# Function that captures the game window based on the saved coords.
def captureWindow():
    global Parameters

    if not Parameters.get("Calculated"):
        print("Window Not Calculated... Skipping Capture")
        return

    window = {
        "top": int(Parameters["TopLeft"][1]),
        "left": int(Parameters["TopLeft"][0]),
        "width": Parameters["Width"],
        "height": Parameters["Height"]
    }

    path = os.path.join("D:\^ Code\Python\GamePlayer\GamePlayer\GameImages", "img.png")
    with mss.mss() as sct:
        screenshot = sct.grab(window)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    img.save(path)
    print("Image Saved")


if __name__ == "__main__":

    # Initilaising new thread called listenerTread to allow
    # for keyboard interactions whilst running other functions.
    listenerThread = th.Thread(target=listener_Thread, daemon=True)
    listenerThread.start()

    # Initilaising new thread called windowThread to allow
    # for the widget to be initialised and do its own process
    # whilst the main thread is carrying out other function.
    windowThread = th.Thread(target=loadWidget_Thread, daemon=True)
    windowThread.start()

    # Making sure that the GameImages dir exists in the file structure
    # if it doesn't make a new dir.

    os.makedirs("D:\^ Code\Python\GamePlayer\GamePlayer\GameImages", exist_ok=True)
    # Loop allowing for continuous program running (Main Thread).
    # Makes sure that all other processes are complete before exiting the program.

    while running:
        Update()
    print("Program Exited")

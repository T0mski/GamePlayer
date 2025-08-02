# Importing Libraries.
import pyautogui as gui
import os
import time
from pynput import keyboard as kb
import threading as th
import tkinter as tk
import MineSweeper
from GUI import GameOverlay
import mss
import mss.tools
from PIL import Image
import pprint

# Declaring Global Variables.
running = True
Parameters = {
    "TopLeft": (1402, 422),
    "BottomRight": (1853, 783),
    "Width": 0.0,
    "Height": 0.0,
    "Calculated": False,
    "Saved": False
}
gridCellWidth = 48
gridCellHeight = 48
gridWidth = 10
gridHeight = 8

TempVariable = False



# Update function that allows the Program to run constantly.
def Update():
    newGrid = captureWindow()
    if newGrid is not None:
        pprint.pp(newGrid)
        MineSweeper.MineSweeperSolver.Solve(newGrid)
    time.sleep(0.5)



# function that is called on the Keyboard Listener Thread of the program.
def listener_Thread():
    def on_press(key):
        global running
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
        if key == kb.Key.shift_l:
            TopLeft = Parameters["TopLeft"]
            BottomRight = Parameters["BottomRight"]
            width = BottomRight[0] - TopLeft[0]
            Parameters["Width"] = width
            height = BottomRight[1] - TopLeft[1]
            Parameters["Height"] = height
            Parameters["Calculated"] = True
            print("Calculating...")
            print(Parameters["TopLeft"], Parameters["BottomRight"])
    with kb.Listener(on_press=on_press) as listener:
        listener.join()



# function that is called on the Load widget Thread of the program.
def loadWidget_Thread():
    def createWindow():
        root = tk.Tk()
        GameOverlay(root)
        root.mainloop()


    createWindow()



# Function that captures the game window based on the saved cords.
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

    path = os.path.join("D:\Coding Projects\GamePlayer\GameImages", "GameImg.png")
    with mss.mss() as sct:
        screenshot = sct.grab(window)
        GameImg = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    GameImg.save(path)
    newGrid = MineSweeper.MineSweeperImageProcessing.analyseImg()
    print("Image Saved")
    return newGrid


if __name__ == "__main__":


    # Initialising new thread called listenerTread to allow
    # for keyboard interactions whilst running other functions.
    listenerThread = th.Thread(target=listener_Thread, daemon=True)
    listenerThread.start()

    # Initialising new thread called windowThread to allow
    # for the widget to be initialised and do its own process
    # whilst the main thread is carrying out other function.
    #
    windowThread = th.Thread(target=loadWidget_Thread, daemon=True)
    windowThread.start()

    # Loop allowing for continuous program running (Main Thread).
    # Makes sure that all other processes are complete before exiting the program.

    while running:
        Update()

    print("Program Exited")

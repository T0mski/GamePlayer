# Importing Libraries.
import pyautogui as gui
import os
import time
from pynput import keyboard as kb
import threading as th
import tkinter as tk
from GUI import GameOverlay
import mss
import mss.tools
from PIL import Image
import cv2
import easyocr as ocr
import numpy as np
import torch
# Declaring Global Variables.
running = True
TopLeft = ()
BottomRight = ()
Parameters = {
    "TopLeft": (1351, 426),
    "BottomRight": (1797, 786),
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



# Update function that allows the Program to run constanly.
def Update():
    img = captureWindow()
    newGrid = analyseImg()
    if newGrid != None:
        for r in newGrid:
            print(r)
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
#def loadWidget_Thread():
#    def createWindow():
#        root = tk.Tk()
#        app = GameOverlay(root)
#        root.mainloop()


#    createWindow()



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
    Parameters["Saved"] = True
    print("Image Saved")


def analyseImg():
    if not Parameters["Saved"]: return

    readpath  = os.path.join("D:\^ Code\Python\GamePlayer\GamePlayer\GameImages\img.png")
    img = cv2.imread(readpath)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    savepath = os.path.join("D:\^ Code\Python\GamePlayer\GamePlayer\GameImages", "Greyscale.png")
    greySave = Image.fromarray(grey)
    greySave.save(savepath)
    _, binary = cv2.threshold(grey, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    binaryImage = Image.fromarray(binary)
    binarySavePath = os.path.join("D:\^ Code\Python\GamePlayer\GamePlayer\GameImages", "Binary.png")
    binaryImage.save(binarySavePath)
    ROWS, COLS = 8, 10
    height, width = binary.shape
    cell_h , cell_w = height // ROWS, width // COLS
    reader = ocr.Reader(["en"])


    result = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            y1, y2 = i * cell_h, (i + 1) * cell_h
            x1, x2 = j * cell_w, (j + 1) * cell_w
            cell_img = binary[y1:y2, x1:x2]
            ocr_result = reader.readtext(cell_img)
            DebugImg = Image.fromarray(cell_img)
            DebugSave(DebugImg,i,j)
            if ocr_result != []:
                text = ocr_result[0][1]
                if text.isdigit() and int(text) < 9:
                    row.append(text)
                elif int(text) > 8:
                    print(f"Error: Value Too Large. Value: {text}, Location: {i, j},")
                    exit(1)
                else:
                    print(f"Error: Value Not Recognised. Value: {text}, Location: {i,j},")
                    DebugPath = os.path.join("D:\^ Code\Python\GamePlayer\GamePlayer\GameImages", "Debug.png")
                    cellImg = Image.fromarray(cell_img)
                    cellImg.save(DebugPath)
                    exit(1)
            elif ocr_result == []:
                row.append("H")
            else:
                print(f"Error: Value Not Recognised. Value: {text}, Location: {i,j},")
                exit(1)
        result.append(row)





    print(result)

def DebugSave(image, indexI, indexJ):
    filename = f"{indexI}{indexJ}.png"
    path = os.path.join("D:\^ Code\Python\GamePlayer\GamePlayer\GameImages\DebugFolder", filename)

    image.save(path)


if __name__ == "__main__":


    # Initilaising new thread called listenerTread to allow
    # for keyboard interactions whilst running other functions.
    listenerThread = th.Thread(target=listener_Thread, daemon=True)
    listenerThread.start()

    ## Initilaising new thread called windowThread to allow
    ## for the widget to be initialised and do its own process
    ## whilst the main thread is carrying out other function.
    ##
    #windowThread = th.Thread(target=loadWidget_Thread, daemon=True)
    #windowThread.start()

    # Making sure that the GameImages dir exists in the file structure
    # if it doesn't make a new dir.

    os.makedirs("D:\^ Code\Python\GamePlayer\GamePlayer\GameImages", exist_ok=True)
    # Loop allowing for continuous program running (Main Thread).
    # Makes sure that all other processes are complete before exiting the program.

    while running:
        Update()

    print("Program Exited")

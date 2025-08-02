import os
import time

import mss
import mss.tools
import pyautogui as gui
from PIL import Image
import cv2
import easyocr as ocr
import numpy as np
import torch
import pprint

TILESIZE = 48
Parameters = {
    "TopLeft": (1402, 422),
    "BottomRight": (1853, 783),
    "Width": 0.0,
    "Height": 0.0,
    "Calculated": False,
    "Saved": False
}
class MineSweeperImageProcessing:
    def analyseImg():
        readpath  = os.path.join("D:\Coding Projects\GamePlayer\GameImages", "GameImg.png")
        img = cv2.imread(readpath)
        grey = cv2.cvtColor(cv2.imread(readpath), cv2.COLOR_BGR2GRAY)


        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

        _, binary = cv2.threshold(grey, 128, 255, cv2.THRESH_BINARY_INV)

        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        ROWS, COLS = 8, 10
        height, width = binary.shape
        cell_h , cell_w = height // ROWS, width // COLS
        reader = ocr.Reader(["en"])

        result = []
        for i in range(ROWS):
            row = []
            for j in range(COLS):

                pad_h = int(cell_h * 0.12)
                pad_w = int(cell_w * 0.2)

                y1, y2 = i * cell_h + pad_h, (i + 1) * cell_h - pad_h
                x1, x2 = j * cell_w + pad_w, (j + 1) * cell_w - pad_w


                cell_img = binary[y1:y2, x1:x2]

                ocr_result = reader.readtext(cell_img, allowlist="01234568")

                DebugImg = Image.fromarray(cell_img)
                DebugTools.DebugSave(image=DebugImg,indexI=i,indexJ=j)
                if ocr_result != []:
                    text = ocr_result[0][1]
                    if text.isdigit():
                        if   int(text) < 9:
                            row.append(text)
                        else:
                            print(f"Error: Value Too Large . Value: {text}, Location: {i, j},")
                            exit(1)
                    elif text == ",":
                        continue
                    else:
                        print(f"Error: Invalid Value. Value: {text}, Location: {i,j},")
                        exit(1)
                else:
                    currentCell =  img[y1:y2, x1:x2]
                    w, h = currentCell.shape[:2]
                    centre = currentCell[h//2, w//2]
                    if (centre == np.array([81,215,170])).all() or (centre == np.array([73,209,162])).all() :
                        row.append("H")
                    else:
                        row.append("O")

            result.append(row)
        return result



class DebugTools:
    def DebugSave(image, indexI=None, indexJ=None, fileName=None):
        if fileName != None:
            filename = fileName
            path = os.path.join("D:\Coding Projects\GamePlayer\GameImages\DebugFolder", filename)
            image.save(path)

        else:
            filename = f"{indexI}{indexJ}.png"
            path = os.path.join("D:\Coding Projects\GamePlayer\GameImages\DebugFolder", filename)
            image.save(path)


DIRECTIONS = [(-1,-1),(-1,0),(-1, 1),
              ( 0,-1),       ( 0, 1),
              ( 1,-1),( 1,0),( 1, 1)]


class MineSweeperSolver:
    def LeftClick(TopLeft, x, y):
        gui.click(TopLeft[0] + y * TILESIZE, TopLeft[1] + x * TILESIZE, button="left")

    def RightClick(TopLeft, x, y):
        gui.click(TopLeft[0] + y * TILESIZE, TopLeft[1] + x * TILESIZE, button="right")

    def GetNeighbours(x, y, width, height):
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width:
                yield nx, ny

    def Solve(currentBoard):
        height = len(currentBoard)
        width = len(currentBoard[0])
        changed = True

        while changed:
            changed = False
            for x in range(height):
                for y in range(width):
                    try:
                        val = int(currentBoard[x][y])
                        if val in range(1, 9):
                            neighbors = list(MineSweeperSolver.GetNeighbours(x, y, width, height))

                            unopened = [(nx, ny) for nx, ny in neighbors if currentBoard[nx][ny] == "H"]
                            flagged = [(nx, ny) for nx, ny in neighbors if currentBoard[nx][ny] == "F"]

                            print(f"[{x}, {y}] → Val: {val} | Unopened: {unopened} | Flagged: {flagged}")

                            # Flagging logic
                            if len(unopened) > 0 and val - len(flagged) == len(unopened):
                                for nx, ny in unopened:
                                    if currentBoard[nx][ny] != "F":
                                        currentBoard[nx][ny] = "F"
                                        MineSweeperSolver.RightClick(Parameters["TopLeft"], nx, ny)
                                        changed = True

                            # Opening logic
                            if val < len(flagged) and len(unopened) > 0:
                                for nx, ny in unopened:
                                    if currentBoard[nx][ny] == "H":
                                        currentBoard[nx][ny] = "0"  # Marked as opened
                                        MineSweeperSolver.LeftClick(Parameters["TopLeft"], nx, ny)
                                        changed = True

                    except ValueError:
                        continue
                    except Exception as e:
                        print(f"There was a {type(e).__name__} error: {e}")




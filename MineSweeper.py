import os
import mss
import mss.tools
from PIL import Image
import cv2
import easyocr as ocr
import numpy as np
import torch


class MineSweeperImageProcessing:
    def analyseImg():
        readpath  = os.path.join("D:\\^ Code\\Python\\GamePlayer\\GamePlayer\\GameImages", "GameImg.png")

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
                DebugSave(DebugImg,i,j)
                if ocr_result != []:
                    text = ocr_result[0][1]
                    if text.isdigit():
                        if   int(text) < 9:
                            row.append(text)
                        else:
                            print(f"Error: Value Too Large . Value: {text}, Location: {i, j},")
                            exit(1)
                    else:
                        print(f"Error: Invalid Value. Value: {text}, Location: {i,j},")
                        exit(1)
                else:
                    row.append("H")

            result.append(row)
        return result



def DebugSave(image, indexI, indexJ):
    filename = f"{indexI}{indexJ}.png"
    path = os.path.join("D:\\^ Code\\Python\\GamePlayer\\GamePlayer\\GameImages\\DebugFolder", filename)

    image.save(path)





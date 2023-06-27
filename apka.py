import cv2 as cv
import numpy as np
import tensorflow as tf
from pytesseract import pytesseract

pytesseract.tesseract_cmd = "C:\\tesseract\\tesseract.exe"
haystack_img = cv.imread('zrzut.jpg', cv.THRESH_BINARY)

nazwy = np.array([
    "Dzika marchew", 
    "Tymianek wąskolistny",
    "Złota porzeczka",
    "Krwawnik pospolity",
    "Jeżyna",
    "Tytoń indysjki",
    "Jagoda",
    "Malina",
    "Podgrzybek",
    "Szałwia kolczasta",
    "Czarna porzeczka",
    "Pomarańcza",
    "Czubajka kania",
    "Mak preriowy",
    "Szałwia kalifornijska",
    "Żeń-Szeń amerykański",
    "Korzeń łopianu",
    "Szałwia pustynna",
    "Złocień maruna",
    "Oregano",
])

for i in range(1, 21):
    needle_img = cv.imread(str(i) + '.jpg', cv.THRESH_BINARY)

    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]

        top_left = max_loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

        # cv.rectangle(haystack_img, top_left, bottom_right, color = (0, 0, 255), thickness = 2, lineType=cv.LINE_4)

        digits = pytesseract.image_to_string(haystack_img[top_left[1] + 75:bottom_right[1] - 15, top_left[0] + 69:bottom_right[0] - 13], lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        # cv.imshow('img', img[top_left[1] + 75:bottom_right[1] - 15, top_left[0] + 68:bottom_right[0] - 13])
        print(nazwy[i-1] + " - " + digits, end = "")



cv.imshow('result', haystack_img)
cv.waitKey()
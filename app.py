from ctypes import alignment
from multiprocessing.sharedctypes import Value
from tkinter.messagebox import showerror, showinfo
from lib2to3.pgen2.token import LEFTSHIFT
from tkinter import filedialog as fd
from tkinter import *
from tkinter import ttk
import tkinter as tk
from turtle import position, width
import cv2 as cv
import numpy as np
import tensorflow as tf
from pytesseract import pytesseract
from numpy import column_stack

def selectFile():
    CopyToClp.config(state=DISABLED)
    global file
    file = fd.askopenfilename().split("/")[-1].strip()

    if file.lower().endswith('.jpg'):
        Count.config(state=NORMAL)
        return file
    else:
        showerror("Błąd", "Niepoprawny format pliku")
        Count.config(state=DISABLED)
        return None
        
def countItems():
    if Name == None:
        showerror("Błąd", "Nie podano imienia i nazwiska")
        return None
    else:
        global NameStr
        NameStr = Name.get()
    pytesseract.tesseract_cmd = "C:\\tesseract\\tesseract.exe"
    haystack_img = cv.imread(file, cv.THRESH_BINARY)

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
    global value
    value = ""
    value = NameStr + "\n"

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

            value += nazwy[i - 1] + ": " + digits

    valueStr.set(value)
    CopyToClp.config(state=NORMAL)

    cv.imshow('result', haystack_img)
    cv.waitKey()

win= Tk()
win.title("Licznik")

valueStr = tk.StringVar()

win.columnconfigure(1, minsize = 100)
win.columnconfigure(1, minsize = 50)

win.geometry("500x500")
win.tk.call('tk', 'scaling', 1.5)

label=Label(win, text="Podaj imię i nazwisko:", font=("Arial", 8))
label.grid(column=0, row=0, sticky = N)

Name= Entry(win, width= 15)
Name.focus_set()
Name.grid(column=0, row=1, sticky = N)

SelectF = Button(win, text= "Wybierz plik", width= 15, command= selectFile)
SelectF.grid(column=0, row=2, sticky = N)

Count = Button(win, text= "Podlicz", width= 15, command= countItems, state = DISABLED)
Count.grid(column=0, row=3, sticky = N)

CopyToClp = Button(win, text= "Kopiuj do schowka", width= 15, command= lambda: win.clipboard_append(valueStr.get()), state = DISABLED)
CopyToClp.grid(column=0, row=4, sticky = N)


labelValue = Label(win, width= 50, height = 50, anchor="nw", textvariable = valueStr)
labelValue.focus_set()
labelValue.place(x = 130, y = -3)



win.mainloop()
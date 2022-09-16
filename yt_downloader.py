# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

from ast import main
from cProfile import label
from mimetypes import init
from re import A
from tkinter.tix import ROW
from turtle import color
from pytube import YouTube
from pytube import Playlist
import tkinter as tk
import os

BG_COLOR = "#181818"
FG_COLOR = "#A80000"
COL_SIZE = 5
ROW_SIZE = 5


def init_root():
    root = tk.Tk()
    root.title("Youtube downloader and cd burner")
    root.configure(bg=BG_COLOR)
    for i in range(COL_SIZE):
        root.columnconfigure(i, weight=1, minsize=75)
        for j in range(ROW_SIZE):
            root.rowconfigure(j, weight=1, minsize=50)

    return root


def menu():
    welcome_label = tk.Label(text="welcome!", font=(
        "Arial", "25"), fg=FG_COLOR, bg=BG_COLOR)
    welcome_label.grid(column=2, row=0)
    title_label = tk.Label(text="YouTube downloader", font=(
        "Arial", "25"), fg=FG_COLOR, bg=BG_COLOR)
    title_label.grid(column=0, row=0)
    menu = []
    for i in range(1, ROW_SIZE):
        btn = tk.Button(text="click", fg=FG_COLOR,
                        command=lambda: change(welcome_label))
        btn.grid(row=i, column=0)
        menu.append(btn)
    menu[0].configure(text="")


def main():
    root = init_root()
    menu()
    root.mainloop()


if __name__ == '__main__':
    main()

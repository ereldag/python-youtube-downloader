# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

from pytube import YouTube
from pytube import Playlist
import tkinter as tk
import os

BG_COLOR = "#181818"
FG_COLOR = "#A80000"
COL_SIZE = 5
ROW_SIZE = 5
menu = []
root = tk.Tk()


def init_root():
    root.title("Youtube downloader and cd burner")
    root.configure(bg=BG_COLOR)
    for i in range(COL_SIZE):
        root.columnconfigure(i, weight=1, minsize=75)
        for j in range(ROW_SIZE):
            root.rowconfigure(j, weight=1, minsize=50)

    create_menu()
    return root


def create_menu():
    # welcome_label = tk.Label(text="welcome!", font=(
    #    "Arial", "25"), fg=FG_COLOR, bg=BG_COLOR)
    #welcome_label.grid(column=2, row=0)
    title_label = tk.Label(master=root, text="YouTube downloader", font=(
        "Arial", "25"), fg=FG_COLOR, bg=BG_COLOR)
    title_label.grid(column=0, row=0)

    menu_frame = tk.Frame(master=root,width='100%',height='100%')
    menu_frame.grid(column=0, row=1, rowspan=4)
    global menu
    for i in range(1, 5):
        btn = tk.Button(master=menu_frame, text="click", fg=FG_COLOR,
                        command=lambda: print("clicked"))
        btn.grid(row=i, column=0)
        menu.append(btn)
    #menu[0].configure(text="")


def main():
    root = init_root()
    root.mainloop()


if __name__ == '__main__':
    main()

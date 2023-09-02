# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

from csv import reader
import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import os
import threading
import sys
from mutagen.easyid3 import EasyID3
from moviepy.editor import *
# ----------- download functions -----------


def write_output(message="", newlines=1):

    lock.acquire()
    # output.print(message+('\n'*newlines))
    window['-OUT-'].print(message+('\n'*newlines))
    lock.release()


# update progress bar
def update_progress_bar(pb, text, finished, count):
    lock.acquire()

    # calculate percentage of completed songs
    percent = round((finished/count)*100)
    pb.update(percent)
    text.update(f"finished {finished} out of {count}")

    lock.release()


def download_song(url, count, file_path, file_name=""):
    if file_path == "":
        file_path = os.getcwd()
    if not os.path.exists(file_path):
        write_output('failed - path not found!')
        # TODO: add validation output
    else:
        try:
            yt = YouTube(url)

            # give title to files with no name, and append .mp3 to file names without type
            if file_name == "":
                file_name = yt.title + ".mp4"
            elif '.' not in file_name:
                file_name = file_name + ".mp4"
            file_name = f"{count:03}-"+file_name
            # write output to gui
            write_output(
                f'downloading "{yt.title}" as "{file_path}\\{file_name}" ')

            # download
            yt.streams.get_audio_only().download(filename=file_name, output_path=file_path)

            mp4_without_frames = AudioFileClip(rf"{file_path}\{file_name}")
            mp4_without_frames.write_audiofile(
                rf"{file_path}\{file_name}".replace('mp4', 'mp3'))
            mp4_without_frames.close()
            os.remove(rf"{file_path}\\{file_name}")
            f = EasyID3(rf"{file_path}\\{file_name}".replace('mp4', 'mp3'))
            f['title'] = yt.title
            f['artist'] = yt.author
            f.save()

            # write success to gui
            write_output('success!', newlines=2)

        except Exception as e:

            # write exception to gui
            write_output('failed... view error message below')
            write_output(f'{e.args}', newlines=2)


def download_single_song(action, values):
    url = values[f'-IN-{action}-URL-']
    file_name = values[f'-IN-{action}-name-']
    file_path = values[f'-IN-{action}-path-']

    # download song
    download_song(url, file_path, file_name)
    write_output(newlines=2)


def download_csv_songs(action, values):
    csv_path = values[f'-IN-{action}-file-']

    pb = window[f"-PROG-{action}-"]
    pb_text = window[f"-PROG-TEXT-{action}-"]

    with open(csv_path, newline='') as csv:
        count = sum(1 for line in csv)

    finished = 0

    update_progress_bar(pb, pb_text, finished, count)

    write_output(f'reading csv "{csv_path}"...')
    # read csv and download specified songs
    with open(csv_path, newline='') as csv:
        for line in reader(csv):
            file_name = line[0].replace('\t', '')
            file_path = line[1]
            url = line[2]
            download_song(url, file_path, file_name)

            finished += 1
            update_progress_bar(pb, pb_text, finished, count)

    write_output(f'finished reading "{csv_path}"!', newlines=2)


def download_playlist(action, values):
    url = values[f'-IN-{action}-url-']
    file_path = values[f'-IN-{action}-path-']

    # create playlist and download each song inside
    plist = Playlist(url)

    pb = window[f"-PROG-{action}-"]
    pb_text = window[f"-PROG-TEXT-{action}-"]

    count = plist.length
    finished = 0
    write_output(f'downloading playlist "{plist.title}"')
    update_progress_bar(pb, pb_text, finished, count)

    for url in plist.video_urls:

        download_song(url, file_path=file_path, count=(finished+1))
        finished += 1
        update_progress_bar(pb, pb_text, finished, count)

    write_output(
        f'finished downloading playlist "{plist.title}"!', newlines=2)

# ----------- functions to create the layouts this Window will display -----------


# layout for single song
def create_single_song_layout(action):
    layout = [[sg.Text("Youtube song URL:", size=(15, 1)), sg.InputText(
        key=f'-IN-{action}-URL-')],
        [sg.Text("File name:", size=(15, 1)), sg.InputText(
            key=f'-IN-{action}-name-')],
        [sg.Text("Download location:", size=(15, 1), justification="left"), sg.Text(), sg.FolderBrowse(
            key=f'-IN-{action}-path-')]]
    return sg.Tab(action, layout, key=f'{action}', border_width=10, element_justification="l")


# layout for csv
def create_csv_layout(action):
    layout = [[sg.Text("CSV location:", size=(15, 1)), sg.Text(), sg.FileBrowse(
        key=f'-IN-{action}-file-', file_types=(("comma seperated values", "*.csv"),),)],
        [sg.ProgressBar(key=f'-PROG-{action}-', max_value=100,
                        size=(30, 15)), sg.Text(key=f"-PROG-TEXT-{action}-")]]
    return sg.Tab(action, layout, key=f'{action}', border_width=10, element_justification="l")


# layout for playlist
def create_playlist_layout(action):
    layout = [[sg.Text("youtube playlist URL:", size=(15, 1)),
               sg.InputText(key=f'-IN-{action}-url-')],
              [sg.Text("download location:", size=(15, 1)), sg.Text(), sg.FolderBrowse(
                  key=f'-IN-{action}-path-')],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=100,
                              size=(30, 15)), sg.Text(key=f"-PROG-TEXT-{action}-")]]
    return sg.Tab(action, layout, key=f'{action}', border_width=10, element_justification="l")


# --------------------------------------------------------------------------------

def main():

    # set theme
    sg.theme("DarkBrown4")

    # ----------- Create layout using specified functions and index
    MENU = {"download single song": [create_single_song_layout, download_single_song],
            "download songs from csv": [create_csv_layout, download_csv_songs],
            "download playlist": [create_playlist_layout, download_playlist]}

    tabs = []
    for action, func in MENU.items():
        tabs.append(func[0](action))
    tabgrp = sg.TabGroup([tabs], tab_location="centertop",
                         border_width=5, enable_events=True)

    # add icon path after pyinstaller conversion
    try:
        icon_path = sys._MEIPASS + '\icons\logo.ico'
    except:
        icon_path = r'icons/logo.ico'

    # create window
    layout = [[sg.Push(), tabgrp, sg.Push()],
              [sg.Push(), sg.Multiline(
                  key='-OUT-', size=(70, 10), autoscroll=True), sg.Push()],
              [sg.Push(), sg.Submit(key='-SUB-'), sg.Push()]]
    global window
    window = sg.Window('youtube downloader', layout, icon=icon_path)

    # create thread lock
    global lock
    lock = threading.Lock()

    # event loop
    while True:
        event, values = window.read()

        # quit
        if event in (None, 'Exit'):
            break

        # call current tab download func
        if str(event) == '-SUB-':
            current_action = values[0]
            threading.Thread(target=MENU[current_action][1], args=(
                current_action, values)).start()

        print(
            f"\n\n------------------------------\n\naction: {values[0]}\nevent: {event}\nvalues: {values}")

    window.close()


# --------------------------------------------------------------------------

if __name__ == '__main__':
    main()

from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from tkinter import messagebox
from tkinter import filedialog
from pygame import mixer
import os
from mutagen.mp3 import MP3
import time
import threading

root = tk.ThemedTk()
root.get_themes()
root.set_theme('plastik')
root.configure(background='orange')
root.minsize(height=700, width=600)


def default_theme():
    global theme
    global fg
    root.get_themes()
    root.set_theme('plastik')
    theme = 'orange'
    fg = 'black'
    musicalabel.configure(image=musicaphoto)
    color()


def aquativo_theme():
    global theme
    global fg
    fg = 'white'
    theme = 'blue'
    root.get_themes()
    root.set_theme('aquativo')
    musicalabel.configure(image=musicaphoto)
    color()


def arc_theme():
    global theme
    global fg
    fg = 'grey'
    theme = 'snow'
    root.get_themes()
    root.set_theme('arc')
    musicalabel.configure(image=musicaphoto)
    color()


def blue_theme():
    global musicablue
    global theme
    global fg
    theme = 'black'
    musicablue = PhotoImage(file='musica_blue.png')
    musicalabel.configure(image=musicablue)
    fg = 'royal blue'
    root.get_themes()
    root.set_theme('blue')
    color()


def orange_theme():
    global theme
    global fg
    theme = 'light goldenrod'
    fg = 'black'
    musicalabel.configure(image=musicaphoto)
    root.get_themes()
    root.set_theme('kroc')
    color()


def radiance_theme():
    global theme
    global fg
    fg = 'grey'
    theme = 'white smoke'
    musicalabel.configure(image=musicaphoto)
    root.get_themes()
    root.set_theme('radiance')
    color()


kirti = Frame(root)
kirti.pack(fill=BOTH, expand=True)

leftframe = Frame(kirti)
leftframe.pack(side=LEFT)

bottomframe = Frame(kirti)
bottomframe.pack(side=BOTTOM)

kirti.configure(background='orange')
leftframe.configure(background='orange')
bottomframe.configure(background='orange')

musicaphoto = PhotoImage(file='musica_big.png')
musicalabel = ttk.Label(bottomframe, image=musicaphoto)
musicalabel.pack(side=TOP, pady=50)
musicalabel.configure(background='orange', foreground='black')

# status bar

statusbar = ttk.Label(root, text='Welcome to MuSica', relief=SUNKEN)
statusbar.pack(side=BOTTOM, fill=X)

# menu bar
menubar = Menu(root)
root.config(menu=menubar)


# create sub menu
def exit_func():
    p = messagebox.askyesno('Confirm Exit', "Do you really want to Exit ?")
    if p == 0:
        return
    else:
        mixer.music.stop()
        root.destroy()


playlist = []


# playlist = contains the full path + filename
# playlistbox = contain just the filename
# fullpath + filename is required to play the music inside play_music function

def file_func():
    global filename
    filename = filedialog.askopenfilename()
    stopbtn.config(state=DISABLED)
    rewindbtn.config(state=DISABLED)
    add_to_playlist(filename)


info_label = ttk.Label(kirti, text='')
info_label.pack(side=TOP, pady=30)
info_label.configure(background='orange', foreground='black')

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=submenu)
submenu.add_command(label='Open', command=file_func)
submenu.add_command(label='Exit', command=exit_func)


def about():
    messagebox.showinfo('About MuSica',
                        '"MUSICA" is an Italian word, which means "MUSIC" in English.\n\nMuSica is a Python based free and open source music player, made by Kirti Sharma.\n\nIt only supports .MP3 and .WAV audio files.\n\nUnlike many music players, MuSica provides you number of Themes to custumize your music player according to you.\n\nYou can add files from your computer to the playlist provided by MuSica and then play unlimited music.')


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Themes', menu=submenu)
submenu.add_command(label='Radiance', command=radiance_theme)
submenu.add_command(label='Aquativo', command=aquativo_theme)
submenu.add_command(label='Arc', command=arc_theme)
submenu.add_command(label='Blue - Black', command=blue_theme)
submenu.add_command(label='Wooden', command=orange_theme)
submenu.add_command(label='Default', command=default_theme)

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=submenu)
submenu.add_command(label='About', command=about)

mixer.init()  # initializing the mixer

root.title('MuSica music player')
root.iconbitmap(r'musica.ico')
stopped = FALSE


def add_to_playlist(f):
    f = os.path.basename(f)
    index = 1000
    playlistbox.insert(index, f)
    playlist.insert(index, filename)
    playlistbox.pack()
    index -= 1


playlistlabel = ttk.Label(leftframe, text='Your Playlist', font='Arial 13 bold')
playlistlabel.pack(pady=5)
playlistlabel.configure(background='orange', foreground='black')

playlistbox = Listbox(leftframe, height=20, width=30)
playlistbox.pack(padx=5)

paused = FALSE
k = 0
v = 0


def play_music():
    global selected_song
    global play_it
    global paused
    global k
    global v
    if paused == TRUE:
        if k == 0:
            mixer.music.pause()
            k = k + 1
            paused = TRUE
            rewindbtn.config(state=DISABLED)
            stopbtn.config(state=DISABLED)
            playbtn.configure(image=playphoto)
            playlistbox.configure(state=NORMAL)
            addbtn.configure(state=NORMAL)
            statusbar['text'] = 'Music Paused : ' + ' ' + os.path.basename(play_it)
            show_details()

        else:
            new_song = playlistbox.curselection()
            new_song = int(new_song[0])
            if new_song == selected_song:
                mixer.music.unpause()
                rewindbtn.config(state=NORMAL)
                stopbtn.config(state=NORMAL)
                playbtn.configure(image=pausephoto)
                playlistbox.configure(state=DISABLED)
                addbtn.configure(state=DISABLED)
                k = 0
                v = 0
                paused = TRUE
                statusbar['text'] = 'Resumed Music : ' + ' ' + os.path.basename(play_it)
                show_details()
            else:
                rewindbtn.config(state=NORMAL)
                stopbtn.config(state=NORMAL)
                play_it = playlist[new_song]
                mixer.music.load(play_it)
                mixer.music.play()
                playlistbox.configure(state=DISABLED)
                playbtn.configure(image=pausephoto)
                k = 0
                v = 1
                selected_song = new_song
                paused = TRUE
                statusbar['text'] = 'Playing Music : ' + ' ' + os.path.basename(play_it)
                info_label['text'] = os.path.basename(play_it)
                show_details()
    else:
        try:
            rewindbtn.config(state=NORMAL)
            stopbtn.config(state=NORMAL)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            playlistbox.configure(state=DISABLED)
            addbtn.configure(state=DISABLED)
            statusbar['text'] = 'Playing Music : ' + ' ' + os.path.basename(play_it)
            playbtn.configure(image=pausephoto)
            info_label['text'] = os.path.basename(play_it)
            paused = TRUE
            show_details()
        except:
            messagebox.showerror('File Not Found',
                                 "Make sure you've selected a file from MuSica playlist and file must be MP3 or WAV")


o = 0


def stop_music():
    global play_it
    global stopped
    global o
    try:
        mixer.music.load(filename)
    except:
        messagebox.showerror('File Not Found', "MuSica couldn't find file. Please try again.")
    else:
        if stopped == TRUE:
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = 'Playing Music : ' + ' ' + ' ' + os.path.basename(play_it)
            stopbtn.configure(image=stopphoto)
            playbtn.config(state=NORMAL)
            rewindbtn.config(state=NORMAL)
            o = 2
            stopped = FALSE
        else:
            mixer.music.stop()
            statusbar['text'] = 'Music Stopped : ' + ' ' + ' ' + os.path.basename(play_it)
            stopbtn.configure(image=playphoto)
            playbtn.config(state=DISABLED)
            rewindbtn.config(state=DISABLED)
            o = 1
            stopped = TRUE


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


r = 0


def rewind_music():
    global r
    if r == 1:
        try:
            mixer.music.load(filename)
        except:
            messagebox.showerror('File Not Found', "MuSica couldn't find file. Please try again.")
        else:
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = 'Music Rewind : ' + ' ' + ' ' + os.path.basename(play_it)
            r = 1
    else:
        try:
            mixer.music.load(filename)
        except:
            messagebox.showerror('File Not Found', "MuSica couldn't find file. Please try again.")
        else:
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = 'Music Rewind : ' + ' ' + ' ' + os.path.basename(play_it)
            r = 1


add_photo = PhotoImage(file='add_music.png')
addbtn = ttk.Button(leftframe, image=add_photo, command=file_func)
addbtn.pack(pady=5)


def show_details():
    file_data = os.path.splitext(play_it)

    if file_data[1] == '.mp3':
        audio = MP3(play_it)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_it)
        total_length = a.get_length()
    min, sec = divmod(total_length, 60)  # quotient and remainder
    min = round(min)
    sec = round(sec)
    timeformat = '{:02d} : {:02d}'.format(min, sec)
    lengthlabel['text'] = timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global k
    global r
    global o
    global v
    x = 0
    b = 100 / t
    while x <= t:
        if k == 1 or o == 1:
            continue
        elif o == 2:
            x = 0
            while x <= t:
                min, sec = divmod(x, 60)  # quotient and remainder
                min = round(min)
                sec = round(sec)
                timeformat = '{:02d} : {:02d}'.format(min, sec)
                current_time_label['text'] = timeformat
                time.sleep(1)
                x = x + 1
                pgbar['value'] = 0
                break
            o = 0
        elif r == 1:
            x = 0
            while x <= t:
                min, sec = divmod(x, 60)  # quotient and remainder
                min = round(min)
                sec = round(sec)
                timeformat = '{:02d} : {:02d}'.format(min, sec)
                current_time_label['text'] = timeformat
                time.sleep(1)
                x = x + 1
                pgbar['value'] = 0
                break
            r = 0
        elif v == 1:
            x = 0
            while x <= t:
                min, sec = divmod(x, 60)  # quotient and remainder
                min = round(min)
                sec = round(sec)
                timeformat = '{:02d} : {:02d}'.format(min, sec)
                current_time_label['text'] = timeformat
                time.sleep(1)
                x = x + 1
                pgbar['value'] = 0
                break
            v = 0
        else:
            min, sec = divmod(x, 60)  # quotient and remainder
            min = round(min)
            sec = round(sec)
            timeformat = '{:02d} : {:02d}'.format(min, sec)
            current_time_label['text'] = timeformat
            time.sleep(1)
            x = x + 1
            for i in range(x):
                pgbar['value'] = i * b


muted = FALSE


def mute_music():
    global muted
    global prev_volume
    if muted == TRUE:
        mixer.music.set_volume(prev_volume)
        volumebtn.configure(image=volumephoto)
        l = int(prev_volume * 100)
        scale.set(l + 1)
        muted = FALSE
    else:
        prev_volume = mixer.music.get_volume()
        mixer.music.set_volume(0)
        volumebtn.configure(image=mutephoto)
        scale.set(0)
        muted = TRUE


scale = ttk.Scale(root, from_=0, to_=100, length=150, orient=HORIZONTAL, command=set_vol)
scale.set(35)
mixer.music.set_volume(0.35)
scale.pack(side=RIGHT, pady=10, padx=10)

mutephoto = PhotoImage(file='002-mute.png')
volumephoto = PhotoImage(file='001-speaker.png')
volumebtn = ttk.Button(root, image=volumephoto, command=mute_music)
volumebtn.pack(side=RIGHT)

lengthlabel = ttk.Label(root, text='00 : 00')
lengthlabel.pack(side=RIGHT, padx=20)
lengthlabel.configure(background='orange', foreground='black')

current_time_label = ttk.Label(root, text='00 : 00')
current_time_label.pack(side=LEFT, padx=10)
current_time_label.configure(background='orange', foreground='black')

pgbar = ttk.Progressbar(root, orient=HORIZONTAL, maximum=100, value=0, mode='determinate')
pgbar.pack(side=BOTTOM, fill=X, pady=10)

rewindphoto = PhotoImage(file='replay.png')
rewindbtn = ttk.Button(bottomframe, image=rewindphoto, command=rewind_music)
rewindbtn.pack(side='left', pady=50)

stopphoto = PhotoImage(file='stop.png')
stopbtn = ttk.Button(bottomframe, image=stopphoto, command=stop_music)
stopbtn.pack(side='right', pady=50)

pausephoto = PhotoImage(file='pause.png')
playphoto = PhotoImage(file='play.png')
playbtn = ttk.Button(bottomframe, image=playphoto, command=play_music)
playbtn.pack(side=BOTTOM, padx=25, pady=50)


def color():
    kirti.configure(bg=theme)
    leftframe.configure(bg=theme)
    bottomframe.configure(bg=theme)
    root.configure(bg=theme)
    lengthlabel.configure(background=theme, foreground=fg)
    current_time_label.configure(background=theme, foreground=fg)
    playlistlabel.configure(background=theme, foreground=fg)
    musicalabel.configure(background=theme)
    info_label.configure(background=theme, foreground=fg)


root.protocol("WM_DELETE_WINDOW", exit_func)

root.mainloop()

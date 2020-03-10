"""
Project name: My Music
Developer: Ali Khodabandehlou

Description:
It's a music player app for windows

start date: 01.03.2020
last edited: 10.03.2020
"""

#import libraries
import tkinter as tk
from PIL import ImageTk,Image
#import eyed3
from mutagen.id3 import ID3
#from mutagen.mp3 import MP3
#from io import BytesIO
import pygame
import tkinter.filedialog as tfd


pygame.init()
#set main windows
myMusic = tk.Tk()
myMusic.title('My Music')
myMusic.iconbitmap('files/img/logo.ico')
myMusic.geometry("250x400")

mainFrame = tk.LabelFrame(myMusic, padx=5, pady=5)
menubar = tk.Menu(myMusic)

#global variables
_paused = False
_playList = 'files/song/playlist.txt'
_currentList = []
_currentListName = ''
_currentListLength = 0
_trackNum = 0


#backward key command
def backward():    
    global _trackNum, _currentList, _paused
    _trackNum -= 1
    if _trackNum < 0 :
        _trackNum = _currentListLength - 1
    pygame.mixer.music.load(_currentList[_trackNum])
    pygame.mixer.music.play()
    
    _paused = False
    playStat = '| |'
    setPage(playStat)


#forward key command
def forward():
    global _trackNum, _currentList, _paused
    _trackNum += 1
    if _trackNum >= _currentListLength :
        _trackNum = 0
    pygame.mixer.music.load(_currentList[_trackNum])
    pygame.mixer.music.play()
    
    _paused = False
    playStat = '| |'
    setPage(playStat)
    

#play key command
def play():
    global _paused
    
    if _paused:
        pygame.mixer.music.unpause()
        _paused = False
    else:
        global _trackNum, _currentList
        pygame.mixer.music.load(_currentList[_trackNum])
        pygame.mixer.music.play()
    
    playStat = '| |'
    setPage(playStat)
    

#pause key command
def pause():
    global _paused
    
    pygame.mixer.music.pause()
    
    _paused = True
    playStat = '>'
    setPage(playStat)
    

#add selected files to playlist
def addPlayList():
    global _trackNum, _paused
    pathToList = []
    filesPath = tfd.askopenfilenames(parent=mainFrame, title='Choose files')
    for filePath in filesPath:
        pathToList.append('\nt ' + str(filePath))
        
    playListFile = open(_playList,'a')
    playListFile.writelines(pathToList)
    playListFile.flush()
    
    loadList()
    

#set main window items
def setPage(playStat = '>'):
    global mainFrame
    
    #load music file
    global _trackNum, _currentList
    musicTrack = ID3(_currentList[_trackNum])
    musicTrackData = musicTrack
    #print(dir(musicTrackData))
    
    #load image
    global songImg
    songImg = ImageTk.PhotoImage(Image.open('files/img/01.png').resize((200, 200)))
    #songImg = Image.open(BytesIO(musicTrackImage))
    songImgLabel = tk.Label(mainFrame, image=songImg)
    
    
    #song info
    songNameLabel = tk.Label(mainFrame, text=musicTrackData['TIT2'].text[0], font='Helvetica 22 bold')
    songAlbumLabel = tk.Label(mainFrame, text=musicTrackData['TALB'].text[0], font='Helvetica 9')
    authorLabel = tk.Label(mainFrame, text=musicTrackData['TPE1'].text[0], font='Helvetica 9')
    
    
    #buttons
    backBtn = tk.Button(mainFrame, text="<<", command=backward)
    forwardBtn = tk.Button(mainFrame, text=">>", command=forward)
    
    if playStat == '>':
        playBtn = tk.Button(mainFrame, text=playStat, command=play)
    else:
        playBtn = tk.Button(mainFrame, text=playStat, command=pause)
    
    loadPage(songImgLabel, songNameLabel, songAlbumLabel, authorLabel, backBtn, forwardBtn, playBtn)


#load page content
def loadPage(songImgLabel, songNameLabel, songAlbumLabel, authorLabel, backBtn, forwardBtn, playBtn):
    global mainFrame, menubar
    
    #pack every item
    myMusic.config(menu=menubar)
    mainFrame.pack(padx=10, pady=10)
    
    songImgLabel.grid(row=0, column=0, columnspan=3, sticky="NEWS")
    songNameLabel.grid(row=1, column=0, columnspan=3, sticky="NEWS", pady=5)
    songAlbumLabel.grid(row=2, column=0, columnspan=3, sticky="NEWS")
    authorLabel.grid(row=3, column=0, columnspan=3, sticky="NEWS", pady=5)
    backBtn.grid(row=4, column=0, sticky="NEWS", pady=3)
    forwardBtn.grid(row=4, column=2, sticky="NEWS", pady=3)
    playBtn.grid(row=4, column=1, sticky="NEWS", pady=3)


#this function loads list of tracks
def loadList():
    global _currentList, _currentListName, _currentListLength
    _currentList.clear()
    _currentListLength = 0
    playListFile = open(_playList,'r')
    tempList = playListFile.read().splitlines()
    for line in tempList:
        line = line.split(' ', 1)
        if line[0] == 't':
            _currentList.append(line[1])
            _currentListLength += 1
        if line[0] == 'n':
            _currentListName = line[1]
    playListFile.flush()


#set menu content
def setMenu():
    global mainFrame, menubar
    
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label='Add to playlist', command=addPlayList)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=mainFrame.quit)
    menubar.add_cascade(label="File", menu=filemenu)


#load program overlay
def loadOverlay():
    setMenu()
    setPage()
    

#start the app
loadList()
loadOverlay()
myMusic.mainloop()

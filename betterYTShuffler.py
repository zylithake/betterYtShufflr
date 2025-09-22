#better yt shuffler

import tkinter as tk
from urllib.request import urlopen
from html.parser import HTMLParser
import webbrowser
import os

from itertools import groupby
from pytube import Playlist
from pytube import Search
import sqlite3 as s3 

searchResult = ""

#Db setup------------------------------------------
#db name
conn = s3.connect('youtubeshuffler.db')


c = conn.cursor()

def playVideo(url):
    webbrowser.open(str(url))



#web parser setup-----------------------------------
class TitleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.match = False
        self.title = ''

    def handle_starttag(self, tag, attributes):
        self.match = tag == 'title'

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False


#adds videos to db from playlist url  | inputs : creator, genre, playlist url
#---------------------------------------------------------------------------
def addPlaylist():
    creatorIN = input("What creator?   ")
    genreIN = input("\nWhat genre?   ")
    creatorIN = creatorIN.lower()#creator
    genreIN = genreIN.lower()#game genre

    plistURL = input("Enter playlist URL:    ")
     # Retrieve URLs of videos from playlist
    playlist = Playlist(plistURL)
    print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

    for url in playlist:
        urlNew = url
        creatorNew = creatorIN
        genreNew = genreIN

        html_string = str(urlopen(urlNew).read())
        parser = TitleParser()
        parser.feed(html_string)
        titleNew = parser.title #title
        titleNew = titleNew.replace("'","") #remove all apostrophes to avoid bug

        c.execute("INSERT INTO videos VALUES (?,?,?,?)",(urlNew,titleNew,creatorNew,genreNew))
        conn.commit()
        
#adds video to db from video url  | inputs : creator, genre, vid url
#---------------------------------------------------------------------------
def addVideo():
    urlN = input("\nEnter url :  ") #url

    html_string = str(urlopen(urlN).read())
    parser = TitleParser()
    parser.feed(html_string)
    titleN = parser.title #title
    titleN = titleN.replace("'","") #remove all apostrophes to avoid bug
    
    creatorN = input("\n Enter creator:  ") #creator
    gameN = input("\n Enter game genre:  ") #game
    
    c.execute("INSERT INTO videos VALUES (?,?,?,?)",(urlN,titleN,creatorN,gameN))
    conn.commit()


#plays one video from specific genre or creator  | inputs: choice of creator or genre, search term for category
#---------------------------------------------------------------------------------------------------------------
def playCat():

    s.pack(side='bottom')
    l.pack()
    e.pack()



    
   

def getPress():
    
    result = e.get(1.0,tk.END + "-1c")
    searchResult = str(result.lower())
    e.delete(1.0,tk.END)
    print(searchResult)
    if searchResult == "creator":
        s1 = tk.Button(window,text="ok",command=lambda: getPress1())
        l1 = tk.Label(window,text = "Enter Creator: ")
        
        l.destroy()
        s.destroy()
        window.update()
        l1.pack(side="left")
        s1.pack(side="bottom")
        
        e.pack()


        result = e.get(1.0,tk.END + "-1c")
        searchResult = str(result.lower())
        

def getPress1():
    result = e.get(1.0,tk.END + "-1c")
    searchResult1 = str(result.lower()) 
    c.execute("SELECT * FROM videos WHERE creator ='"+searchResult1+"'ORDER BY RANDOM();")
    getVid = c.fetchone()
    playVideo(getVid[0])      
        


'''
    elif searchResult == "genre":
        genreS = input("Enter genre: ")
        c.execute("SELECT * FROM videos WHERE game ='"+genreS+"';")
        searchResults = c.fetchone()
        playVideo(searchResults[0])
        '''


#plays random video from whole db  | inputs: none
#---------------------------------------------------------------------------
def playRandomVideo():
    c.execute("SELECT * FROM videos ORDER BY RANDOM();")
    vid = c.fetchone()
    playVideo(vid[0])


#-----------------------------------------------------------------------------------Driver Code-----------------------------------------------------------------------------------------------------------------------




window = tk.Tk()
window.title('Youtube Shuffler')
window.geometry('300x300')
window.config(cursor="star")
window['bg']="#9370DB"

addVideoB = tk.Button(window,text="Add video", command = addVideo)
addPlaylistB = tk.Button(window, text= "Add playlist", command = addPlaylist)
playRandVidB = tk.Button(window, text="Play random video", command= playRandomVideo)
searchCatB = tk.Button(window,text="Search videos by category", command= playCat)

addVideoB.config(width=35, height=3)
addPlaylistB.config(width=35,height=3)
playRandVidB.config(width=35,height=3)
searchCatB.config(width=35,height=3)


l = tk.Label(window,text = "Search by creator or by genre?")
e = tk.Text(window)
s = tk.Button(window,text="ok",command=lambda: getPress())
e.config(height=3,width=40)

searchCatB.pack()
addPlaylistB.pack()
playRandVidB.pack()
addVideoB.pack()

window.mainloop()

conn.close()
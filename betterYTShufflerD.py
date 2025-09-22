#better yt shuffler browser integration?

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
addVurl = ""
addVcr = ""
addVGm = ""

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
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def addPlaylist():
    s = tk.Button(enterUrlScreenP,text="ok",command=lambda: addPlaylist2())
    l = tk.Label(enterUrlScreenP,text = "Enter URL: ")
    mainMenuScreen.pack_forget()
    window.update()
    enterUrlScreenP.pack(side='top')

    s.pack(side='bottom')
    l.pack()
    e.pack()




def addPlaylist2():
    enterUrlScreenP.pack_forget()
    result = e.get(1.0,tk.END + "-1c")

    playlist = Playlist(result)
    s1 = tk.Button(enterCrScreenP,text = "ok", command = lambda : addPlaylist3(playlist))
    l1 = tk.Label(enterCrScreenP,text="Enter creator")
    e.delete(1.0,tk.END)
    e.pack()
    enterCrScreenP.pack()
    s1.pack()
    l1.pack()




def addPlaylist3(playlist):
    enterCrScreenP.pack_forget()
    result = e.get(1.0,tk.END + "-1c")
    creator = str(result)
    enterfinScreenP.pack()
    s2 = tk.Button(enterfinScreenP,text = "ok", command = lambda : addPlaylist4(playlist,creator))
    l2 = tk.Label(enterfinScreenP,text="Enter genre")
    e.delete(1.0,tk.END)
    e.pack()
    s2.pack()
    l2.pack()


def addPlaylist4(playlist,creator):
    enterfinScreenP.pack_forget()
    result = e.get(1.0,tk.END + "-1c")
    genre = str(result)
    processScreenP.pack()
    l3 = tk.Label(processScreenP,text='Now adding...')
    l3.pack()
    e.pack_forget()
    for urlp in playlist:
        window.update()
        urlNew = urlp
        creatorNew = creator
        genreNew = genre

        html_string = str(urlopen(urlNew).read())
        parser = TitleParser()
        parser.feed(html_string)
        titleNew = parser.title #title
        titleNew = titleNew.replace("'","") #remove all apostrophes to avoid bug
        l4 = tk.Label(processScreenP,text = titleNew)
        l4.pack()
        window.update()
        try:
            c.execute("INSERT INTO videos VALUES (?,?,?,?)",(urlNew,titleNew,creatorNew,genreNew))
        except s3.IntegrityError:
            print("unable to add video, may be a duplicate")

        conn.commit()
        l4.pack_forget()
        
    l3.pack_forget()
    finmsg = tk.Label(processScreenP,text='Finished!')
    finmsg.pack()
    window.update()
    






   


#adds video to db from video url  | inputs : creator, genre, vid url
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def addVideo():
    
    s = tk.Button(enterUrlScreen,text="ok",command=lambda: addVideoURLQ())
    l = tk.Label(enterUrlScreen,text = "Enter URL: ")
    mainMenuScreen.pack_forget()
    window.update()
    enterUrlScreen.pack(side='top')

    s.pack(side='bottom')
    l.pack()
    e.pack()



def addVideoURLQ():
    enterCrScreen.pack()
    result = e.get(1.0,tk.END + "-1c")
    addVurl = str(result)
    enterUrlScreen.destroy()
    
    html_string = str(urlopen(addVurl).read())
    parser = TitleParser()
    parser.feed(html_string)
    titleNew = parser.title #title
    titleNew = titleNew.replace("'","") #remove all apostrophes to avoid bug

    e.delete(1.0,tk.END)
    window.update()
    s1 = tk.Button(enterCrScreen,text="ok",command=lambda: addVideoCrQ(addVurl,titleNew))
    l1 = tk.Label(enterCrScreen,text = "Enter creator: ")

    s1.pack(side='bottom')
    l1.pack()
    e.pack()
    window.update()
    

def addVideoCrQ(url,title):
    enterCrScreen.destroy()
    enterfinScreen.pack(side='bottom')
    result = e.get(1.0,tk.END + "-1c")
    addVcr = str(result.lower())
    e.delete(1.0,tk.END)
    
    s2 = tk.Button(enterfinScreen,text="ok",command=lambda: addVideoGrQ(url,title,addVcr))
    l2 = tk.Label(enterfinScreen,text = "Enter genre: ")

    s2.pack()
    l2.pack()
    e.pack()
    window.update()

def addVideoGrQ(url,title,creator):
    processScreen.pack()
    window.update()
    result = e.get(1.0,tk.END + "-1c")
    addVGm = str(result.lower())
    
    e.delete(1.0,tk.END)

    l3 = tk.Label(processScreen,text = "Now Adding...\n" + title)
    l3.config(width=40,height=8,wraplength=280)
    l3.pack()
    window.update()
    c.execute("INSERT INTO videos VALUES (?,?,?,?)",(url,title,creator,addVGm))
    conn.commit()
    


#loads vid to play from category entry
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def playCat():
    catSearchScreen.pack(side='top')
    mainMenuScreen.pack_forget()
    window.update()
    c.execute("SELECT game FROM videos")
    cats = c.fetchall()
    cats = list(set(cats))
    catLab = tk.Label(catSearchScreen12,text = 'Categories:')
    catLab.pack(side='top')
    creLab = tk.Label(creSearchScreen12,text = 'Creators:')
    creLab.pack(side='top')
    for cat in cats:
        catLab1 = tk.Label(catSearchScreen12,text=cat[0])
        catLab1.pack()
    
    c.execute("SELECT creator FROM videos")
    cres = c.fetchall()
    cres = list(set(cres))

    
    for cre in cres:
        creLab1 = tk.Label(creSearchScreen12,text=cre[0])
        creLab1.pack()
    
    

    s.pack(side='bottom')
    l.pack()
    e.pack()



    
   
#gets submitted choice of creator or genre, refreshes and prompts further choice
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def catSearchQ():
    catSearchScreen.pack_forget()
    catSearchScreen1.pack(side='top')
    
    result = e.get(1.0,tk.END + "-1c")
    searchResult = str(result.lower())
    e.delete(1.0,tk.END)

    if searchResult == "creator":
        
        creSearchScreen12.pack(side='bottom')
        s1 = tk.Button(catSearchScreen1,text="ok",command=lambda: creatorSearch())
        l1 = tk.Label(catSearchScreen1,text = "Enter Creator: ")
        
        l.destroy()
        s.destroy()
        window.update()
        l1.pack()
        s1.pack(side="bottom")
        
        e.pack()


        result = e.get(1.0,tk.END + "-1c")
        searchResult = str(result.lower())


    elif searchResult == "genre" or searchResult == "game" or searchResult == "game genre":
        
        catSearchScreen12.pack(side='bottom')
        s1 = tk.Button(catSearchScreen1,text="ok",command=lambda: genreSearch())
        l1 = tk.Label(catSearchScreen1,text = "Enter genre: ")
        
        l.destroy()
        s.destroy()
        window.update()
        l1.pack()
        s1.pack(side="bottom")
        
        e.pack()


        result = e.get(1.0,tk.END + "-1c")
        searchResult = str(result.lower())
        
#gets specific creator query, searches db for that
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def creatorSearch():
    result = e.get(1.0,tk.END + "-1c")
    searchResult1 = str(result.lower()) 
    try:
        c.execute("SELECT * FROM videos WHERE creator ='"+searchResult1+"'ORDER BY RANDOM();")
        getVid = c.fetchone()
        playVideo(getVid[0])  
    except:
        print("Invalid creator query, may not be in database")    

#gets specific genre query, searches db for that
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def genreSearch():
    result = e.get(1.0,tk.END + "-1c")
    searchResult1 = str(result.lower()) 
    try:
        c.execute("SELECT * FROM videos WHERE game ='"+searchResult1+"'ORDER BY RANDOM();")
        getVid = c.fetchone()
        playVideo(getVid[0])  
    except:
        print("Invalid creator query, may not be in database")    

        

#plays random video from whole db  | inputs: none
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def playRandomVideo():
    c.execute("SELECT * FROM videos ORDER BY RANDOM();")
    vid = c.fetchone()
    playVideo(vid[0])


#-----------------------------------------------------------------------------------Driver Code-----------------------------------------------------------------------------------------------------------------------



dest1 = False
dest2 = False


window = tk.Tk()
window.title('Youtube Shuffler')
window.title("Youtube Shuffler")
window.geometry('300x300')
window.config(cursor="star")
window['bg']="#9370DB"

enterUrlScreen = tk.Frame(window)
enterCrScreen = tk.Frame(window)
enterfinScreen = tk.Frame(window)
processScreen = tk.Frame(window)
enterUrlScreenP = tk.Frame(window)
enterCrScreenP = tk.Frame(window)
enterfinScreenP = tk.Frame(window)
processScreenP = tk.Frame(window)
mainMenuScreen = tk.Frame(window)
catSearchScreen = tk.Frame(window)
catSearchScreen1 = tk.Frame(window)
catSearchScreen12 = tk.Frame(window)
creSearchScreen12 = tk.Frame(window)

addVideoB = tk.Button(mainMenuScreen,text="Add video", command = addVideo)
addPlaylistB = tk.Button(mainMenuScreen, text= "Add playlist", command = addPlaylist)
playRandVidB = tk.Button(mainMenuScreen, text="Play random video", command= playRandomVideo)
searchCatB = tk.Button(mainMenuScreen,text="Play video from a category", command= playCat)



addVideoB.config(width=35, height=2)
addPlaylistB.config(width=35,height=2)
playRandVidB.config(width=35,height=2)
searchCatB.config(width=35,height=2)

l = tk.Label(catSearchScreen,text = "Search by creator or by genre?")


e = tk.Text(window)
e.config(height=3,width=40)

mainMenuScreen.pack()
searchCatB.pack()
addPlaylistB.pack()
playRandVidB.pack()
addVideoB.pack()
s = tk.Button(catSearchScreen,text = "ok",command=lambda: catSearchQ())
window.mainloop()



l1 = tk.Label(window,text = "Enter creator: ")
s1 = tk.Button(window,text="ok",command=lambda: addVideoCrQ())
conn.close()
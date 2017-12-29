import sys
from tkinter import *
import tkinter.ttk as ttk

'''Definitions for clickable Graphic Elements(Radiobuttons and Checkbuttons)'''
def set_Tk_var():
    global combobox
    combobox = StringVar()
    global che48
    che48 = StringVar()
    global che49
    che49 = StringVar()
    global che50
    che50 = StringVar()
    global che51
    che51 = StringVar()
'''Root and Toplevel definition'''
def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
'''Function to output errormessage'''
def error_gui(errormessage,errortitle2):
    global val, w, root2
    global emessage
    global errortitle
    emessage = errormessage
    if errortitle2 == None:
        errortitle = 'Error'
    else:
        errortitle = errortitle2
    root2 = Tk()
    top = Errorclass(root2)
    top_level=top
    root2.mainloop()
    
'''Function to output information disapears automatically'''
def message_gui(message2,title2):
    global val, w, root2
    global message
    global title
    message = message2
    if title2 == None:
        title = 'Pythron'
    else:
        title = errortitle2
    root2 = Tk()
    top = Messageclass(root2)
    top_level=top
    root2.after(5000, lambda: root2.destroy())
    root2.mainloop()

    '''Starts first interface(select name and color)'''
def start_gui1():
    global val, w, root 
    root = Tk()
    set_Tk_var()
    top = Lobbygui1class(root)
    init(root, top)
    root.mainloop()
    
    '''Starts second interface(create/join match)'''
def start_gui2(gameslist,serverip):
    global val, w, root
    global serveriptkinter
    global avagameslisttkinter
    serveriptkinter = serverip
    avagameslisttkinter = gameslist
    root = Tk()
    set_Tk_var()
    top = Lobbygui2class (root)
    init(root, top)
    root.mainloop()    

class Errorclass:
    
    '''closes the window'''
    def command_close(self):
        root2.destroy()
        
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # color: gray
        _fgcolor = '#000000'  # color: black
        _compcolor = '#d9d9d9' # color: gray
        _ana1color = '#d9d9d9' # color: gray
        _ana2color = '#d9d9d9' # color: gray

        top.geometry("304x120+624+348")#size definition and placement of the box on display
        top.title(errortitle)#title of the box displayed in headerline
        top.configure(background="#d9d9d9")
        '''Graphic elements configurations'''
        self.Okbutton = Button(top) #Button to close errorwindow
        self.Okbutton.place(relx=0.39, rely=0.75, height=24, width=56)#placement in window using relative positioning
        self.Okbutton.configure(activebackground="#d9d9d9")
        self.Okbutton.configure(activeforeground="#000000")
        self.Okbutton.configure(background="#d9d9d9")
        self.Okbutton.configure(disabledforeground="#a3a3a3")
        self.Okbutton.configure(foreground="#000000")
        self.Okbutton.configure(highlightbackground="#d9d9d9")
        self.Okbutton.configure(highlightcolor="black")
        self.Okbutton.configure(pady="0")
        self.Okbutton.configure(text='''Ok''')
        self.Okbutton.configure(width=56)
        self.Okbutton.configure(command=self.command_close)


        self.Errormessage = Label(top)#Output Errortext
        self.Errormessage.place(relx=0.03, rely=0.25, height=21, width=284)
        self.Errormessage.configure(background="#d9d9d9")
        self.Errormessage.configure(disabledforeground="#a3a3a3")
        self.Errormessage.configure(foreground="#000000")
        self.Errormessage.configure(text=emessage)
        self.Errormessage.configure(width=284)
        
        
class Messageclass:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # color: gray
        _fgcolor = '#000000'  # color: black
        _compcolor = '#d9d9d9' # color: gray
        _ana1color = '#d9d9d9' # color: gray
        _ana2color = '#d9d9d9' # color: gray

        top.geometry("300x120+600+400")
        top.title(title)
        top.configure(background="#d9d9d9")

        self.Xmessage = Label(top)#Output Message
        self.Xmessage.place(relx=0.03, rely=0.25, height=21, width=284)
        self.Xmessage.configure(background="#d9d9d9")
        self.Xmessage.configure(disabledforeground="#a3a3a3")
        self.Xmessage.configure(foreground="#000000")
        self.Xmessage.configure(text=message)
        self.Xmessage.configure(width=284)
    
    
class Lobbygui1class:
    
    global playercolor
    global playername
    
    '''closes the window'''
    def command_close(self):
        namecache = open("pythron_savecache.txt", 'w')
        namecache.write('0')
        namecache.close()
        root.destroy()
        
    '''Saving the inputs and closes the window or output error '''
    def command_next(self):
        self.playername = self.Nameentry.get()
        if self.playername=='': #errormessage if no name is set
            error_gui('Please enter your name',None)
        else:
            self.playercolor= self.color.get() #saving and close window
            namecache = open("pythron_savecache.txt", 'w')
            namecache.write('1 \n'+self.playername +'\n'+ self.playercolor)
            namecache.close()
            root.destroy()
        
        
  
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # color: gray
        _fgcolor = '#000000'  # color: black
        _compcolor = '#d9d9d9' # color: gray
        _ana1color = '#d9d9d9' # color: gray
        _ana2color = '#d9d9d9' # color: gray
        self.style = ttk.Style()
        
       
        if sys.platform == "win32":  #better look for windows systems
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])
        
        top.geometry("400x300+150+150")
        top.title("Pythron_Lobby")
        top.configure(background="#d9d9d9")
        self.Gui1()
        
    def Gui1(self,top=None):
        self.Playerframe = LabelFrame(top)#frame containing all elements for the setup
        self.Playerframe.place(relx=0.03, rely=0.03, relheight=0.72
                , relwidth=0.95)
        self.Playerframe.configure(relief=GROOVE)
        self.Playerframe.configure(foreground="black")
        self.Playerframe.configure(text='''Player''')
        self.Playerframe.configure(background="#d9d9d9")
        self.Playerframe.configure(width=380)
        
        self.Namelabel = ttk.Label(self.Playerframe)#text Player Name
        self.Namelabel.place(relx=0.4, rely=0.14, height=17, width=85)
        self.Namelabel.configure(background="#d9d9d9")
        self.Namelabel.configure(foreground="#000000")
        self.Namelabel.configure(relief=FLAT)
        self.Namelabel.configure(text='''Player Name''')
        
        self.Nameentry = Entry(self.Playerframe)# input field for Player Name
        self.Nameentry.place(relx=0.29, rely=0.23, relheight=0.09, relwidth=0.43)
        self.Nameentry.configure(background="white")
        self.Nameentry.configure(disabledforeground="#a3a3a3")
        self.Nameentry.configure(font="TkFixedFont")
        self.Nameentry.configure(foreground="#000000")
        self.Nameentry.configure(insertbackground="black")
        self.Nameentry.insert(1,'Default')
        
        self.colorlabel = ttk.Label(self.Playerframe) #text Color
        self.colorlabel.place(relx=0.45, rely=0.6, height=19, width=40)
        self.colorlabel.configure(background="#d9d9d9")
        self.colorlabel.configure(foreground="#000000")
        self.colorlabel.configure(relief=FLAT)
        self.colorlabel.configure(text='''Color''')
        
        '''Initialization of Radiobuttons (only one can be selected)'''
        self.colors = ["Green", "Red", "Blue", "Yellow"]
        self.color = combobox
        self.color.set("Red")
        for i in self.colors:
            b=Radiobutton(self.Playerframe)
            b["text"]= i
            b["value"]=i
            b["variable"]= self.color
            b.configure(activebackground="#d9d9d9")
            b.configure(activeforeground="#000000")
            b.configure(background="#d9d9d9")
            b.configure(disabledforeground="#a3a3a3")
            b.configure(foreground="#000000")
            b.configure(highlightbackground="#d9d9d9")
            b.configure(highlightcolor="black")
            b.configure(justify=LEFT)
            #button placement
            if i =="Red":
                b.place(relx=0.3, rely=0.7)
            if i =="Blue":
                b.place(relx=0.3, rely=0.8)
            if i =="Green":
                b.place(relx=0.55, rely=0.7)
            if i =="Yellow":
                b.place(relx=0.55, rely=0.8)
            
        
        self.Closebutton = Button(top) #Button to close window
        self.Closebutton.place(relx=0.05, rely=0.81, height=40, width=100)
        self.Closebutton.configure(activebackground="#d9d9d9")
        self.Closebutton.configure(activeforeground="#000000")
        self.Closebutton.configure(background="#d9d9d9")
        self.Closebutton.configure(disabledforeground="#a3a3a3")
        self.Closebutton.configure(foreground="#000000")
        self.Closebutton.configure(highlightbackground="#d9d9d9")
        self.Closebutton.configure(highlightcolor="black")
        self.Closebutton.configure(pady="0")
        self.Closebutton.configure(text='''Close''')
        self.Closebutton.configure(width=107)
        self.Closebutton.configure(command=self.command_close)
        
        self.Nextbutton = Button(top) #Button to continue with next step
        self.Nextbutton.place(relx=0.68, rely=0.81, height=40, width=100)
        self.Nextbutton.configure(activebackground="#d9d9d9")
        self.Nextbutton.configure(activeforeground="#000000")
        self.Nextbutton.configure(background="#d9d9d9")
        self.Nextbutton.configure(disabledforeground="#a3a3a3")
        self.Nextbutton.configure(foreground="#000000")
        self.Nextbutton.configure(highlightbackground="#d9d9d9")
        self.Nextbutton.configure(highlightcolor="black")
        self.Nextbutton.configure(pady="0")
        self.Nextbutton.configure(text='''Find Server''')
        self.Nextbutton.configure(command=self.command_next)#calls function to save settings 
        
        
class Lobbygui2class:
    
    '''closes the window'''
    def command_close(self):
        namecache = open("pythron_savecache.txt", 'w')
        namecache.write('0')
        namecache.close()
        root.destroy()
        
    '''closes the window and write back 1 to be opened again'''
    def command_refresh(self):
        namecache = open("pythron_savecache.txt", 'w')
        namecache.write('1')
        namecache.close()
        root.destroy()
        
    '''closes window and write back selected match'''
    def command_join(self):
        namecache = open("pythron_savecache.txt", 'w')
        #error handling
        if self.Selectmatchesbox.get()=='':
            error_gui('Please select a match','Error')
        if self.Selectmatchesbox.get()=='No open matches':
            error_gui('You can\'t select No matches','Error')
            
        #write back and close in case of no errors
        else:
            namecache.write('2\n'+self.Selectmatchesbox.get())
            namecache.close()
            root.destroy()
    '''closes window and write back name of created match''' 
    def command_create(self):
        namecache = open("pythron_savecache.txt", 'w')
        #error in case of no entry
        if self.Matchnameentry.get()=='':
            error_gui('Please enter a name for your match','Error')
        
        #write back name of the game and features
        else:
            namecache.write('3\n'+self.Matchnameentry.get()+'\n'+che48.get()+'\n'+che49.get()+'\n'+che50.get()+'\n'+che51.get())
            namecache.close()
            root.destroy()
    
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # color: gray
        _fgcolor = '#000000'  # color: black
        _compcolor = '#d9d9d9' # color: gray
        _ana1color = '#d9d9d9' # color: gray
        _ana2color = '#d9d9d9' # color: gray
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("630x350+400+200")
        top.title("Pythron_Lobby")
        top.configure(background="#d9d9d9")


        
        self.Joinframe = LabelFrame(top)#frame where all elements for joining a game are within
        self.Joinframe.place(relx=0.02, rely=0.03, relheight=0.71, relwidth=0.48)

        self.Joinframe.configure(relief=GROOVE)
        self.Joinframe.configure(foreground="black")
        self.Joinframe.configure(text='''Join Match''')
        self.Joinframe.configure(background="#d9d9d9")
        self.Joinframe.configure(width=300)

        self.Selectmatchesbox = ttk.Combobox(self.Joinframe,state='readonly')#box that displays all matches; player is available to select one
        self.Selectmatchesbox.place(relx=0.08, rely=0.36, relheight=0.12
                , relwidth=0.83)
        self.Selectmatchesbox.configure(textvariable=combobox)
        self.Selectmatchesbox.configure(width=243)
        self.Selectmatchesbox.configure(takefocus="")
        self.Selectmatchesbox["values"]= avagameslisttkinter
        

        self.Avalabel = Label(self.Joinframe)#label for Selectmatchesbox
        self.Avalabel.place(relx=0.33, rely=0.24, height=25, width=120)
        self.Avalabel.configure(background="#d9d9d9")
        self.Avalabel.configure(disabledforeground="#a3a3a3")
        self.Avalabel.configure(foreground="#000000")
        self.Avalabel.configure(text='''Available Matches''')
        self.Avalabel.configure(width=94)

        self.Joinbutton = Button(self.Joinframe)#button to be pressed after selecting a match for joining
        self.Joinbutton.place(relx=0.33, rely=0.76, height=34, width=100)
        self.Joinbutton.configure(activebackground="#d9d9d9")
        self.Joinbutton.configure(activeforeground="#000000")
        self.Joinbutton.configure(background="#d9d9d9")
        self.Joinbutton.configure(disabledforeground="#a3a3a3")
        self.Joinbutton.configure(foreground="#000000")
        self.Joinbutton.configure(highlightbackground="#d9d9d9")
        self.Joinbutton.configure(highlightcolor="black")
        self.Joinbutton.configure(pady="0")
        self.Joinbutton.configure(text='''Join''')
        self.Joinbutton.configure(width=97)
        self.Joinbutton.configure(command=self.command_join)

        self.Createframe = LabelFrame(top)#frame where all elements for creating a game are within
        self.Createframe.place(relx=0.51, rely=0.03, relheight=0.71
                , relwidth=0.48)
        self.Createframe.configure(relief=GROOVE)
        self.Createframe.configure(foreground="black")
        self.Createframe.configure(text='''Create Match''')
        self.Createframe.configure(background="#d9d9d9")
        self.Createframe.configure(width=270)

        self.Createbutton = Button(self.Createframe)#button to be pressed after selecting a name and the features for creating a game
        self.Createbutton.place(relx=0.33, rely=0.76, height=34, width=100)
        self.Createbutton.configure(activebackground="#d9d9d9")
        self.Createbutton.configure(activeforeground="#000000")
        self.Createbutton.configure(background="#d9d9d9")
        self.Createbutton.configure(disabledforeground="#a3a3a3")
        self.Createbutton.configure(foreground="#000000")
        self.Createbutton.configure(highlightbackground="#d9d9d9")
        self.Createbutton.configure(highlightcolor="black")
        self.Createbutton.configure(pady="0")
        self.Createbutton.configure(text='''Create''')
        self.Createbutton.configure(command=self.command_create)

        self.Matchnameentry = Entry(self.Createframe)#player can write the name of the match in here
        self.Matchnameentry.place(relx=0.17, rely=0.2, relheight=0.08
                , relwidth=0.67)
        self.Matchnameentry.configure(background="white")
        self.Matchnameentry.configure(disabledforeground="#a3a3a3")
        self.Matchnameentry.configure(font="TkFixedFont")
        self.Matchnameentry.configure(foreground="#000000")
        self.Matchnameentry.configure(insertbackground="black")
        self.Matchnameentry.configure(width=174)

        self.Matchlabel = Label(self.Createframe)#title for Matchnameentry
        self.Matchlabel.place(relx=0.33, rely=0.08, height=25, width=100)
        self.Matchlabel.configure(background="#d9d9d9")
        self.Matchlabel.configure(disabledforeground="#a3a3a3")
        self.Matchlabel.configure(foreground="#000000")
        self.Matchlabel.configure(text='''Match Name''')
        self.Matchlabel.configure(width=95)

        self.Featurelabel = Label(self.Createframe)#Title for the four featurebuttons
        self.Featurelabel.place(relx=0.37, rely=0.36, height=25, width=70)
        self.Featurelabel.configure(background="#d9d9d9")
        self.Featurelabel.configure(disabledforeground="#a3a3a3")
        self.Featurelabel.configure(foreground="#000000")
        self.Featurelabel.configure(text='''Features''')
        self.Featurelabel.configure(width=70)

        
        self.Checkbutton1 = Checkbutton(self.Createframe)#Button for selecting feature1 (slow)
        self.Checkbutton1.place(relx=0.27, rely=0.56, relheight=0.1
                , relwidth=0.27)
        self.Checkbutton1.configure(activebackground="#d9d9d9")
        self.Checkbutton1.configure(activeforeground="#000000")
        self.Checkbutton1.configure(background="#d9d9d9")
        self.Checkbutton1.configure(disabledforeground="#a3a3a3")
        self.Checkbutton1.configure(foreground="#000000")
        self.Checkbutton1.configure(highlightbackground="#d9d9d9")
        self.Checkbutton1.configure(highlightcolor="black")
        self.Checkbutton1.configure(justify=LEFT)
        self.Checkbutton1.configure(text='''Slow''')
        self.Checkbutton1.configure(onvalue='ON')
        self.Checkbutton1.configure(offvalue='OFF')
        self.Checkbutton1.configure(variable=che48)
        self.Checkbutton1.deselect()

        self.Checkbutton2 = Checkbutton(self.Createframe)#Button for selecting feature2 (Walls)
        self.Checkbutton2.place(relx=0.57, rely=0.56, relheight=0.1
                , relwidth=0.27)
        self.Checkbutton2.configure(activebackground="#d9d9d9")
        self.Checkbutton2.configure(activeforeground="#000000")
        self.Checkbutton2.configure(background="#d9d9d9")
        self.Checkbutton2.configure(disabledforeground="#a3a3a3")
        self.Checkbutton2.configure(foreground="#000000")
        self.Checkbutton2.configure(highlightbackground="#d9d9d9")
        self.Checkbutton2.configure(highlightcolor="black")
        self.Checkbutton2.configure(justify=LEFT)
        self.Checkbutton2.configure(text='''Walls''')
        self.Checkbutton2.configure(onvalue='ON')
        self.Checkbutton2.configure(offvalue='OFF')
        self.Checkbutton2.configure(variable=che49)
        self.Checkbutton2.deselect()
        
        self.Checkbutton3 = Checkbutton(self.Createframe)#Button for selecting feature3 (fast)
        self.Checkbutton3.place(relx=0.27, rely=0.46, relheight=0.1
                , relwidth=0.27)
        self.Checkbutton3.configure(activebackground="#d9d9d9")
        self.Checkbutton3.configure(activeforeground="#000000")
        self.Checkbutton3.configure(background="#d9d9d9")
        self.Checkbutton3.configure(disabledforeground="#a3a3a3")
        self.Checkbutton3.configure(foreground="#000000")
        self.Checkbutton3.configure(highlightbackground="#d9d9d9")
        self.Checkbutton3.configure(highlightcolor="black")
        self.Checkbutton3.configure(justify=LEFT)
        self.Checkbutton3.configure(text='''Fast''')
        self.Checkbutton3.configure(onvalue='ON')
        self.Checkbutton3.configure(offvalue='OFF')
        self.Checkbutton3.configure(variable=che50)
        self.Checkbutton3.deselect()
        
        self.Checkbutton4 = Checkbutton(self.Createframe)#unused 
        self.Checkbutton4.place(relx=0.57, rely=0.46, relheight=0.1
                , relwidth=0.27)
        self.Checkbutton4.configure(activebackground="#d9d9d9")
        self.Checkbutton4.configure(activeforeground="#000000")
        self.Checkbutton4.configure(background="#d9d9d9")
        self.Checkbutton4.configure(disabledforeground="#a3a3a3")
        self.Checkbutton4.configure(foreground="#000000")
        self.Checkbutton4.configure(highlightbackground="#d9d9d9")
        self.Checkbutton4.configure(highlightcolor="black")
        self.Checkbutton4.configure(justify=LEFT)
        self.Checkbutton4.configure(text='''Feature 4''')
        self.Checkbutton4.configure(onvalue='ON')
        self.Checkbutton4.configure(offvalue='OFF')
        self.Checkbutton4.configure(variable=che51)
        self.Checkbutton4.deselect()

        self.Refreshbutton = Button(top)#button to be pressed for command_refresh
        self.Refreshbutton.place(relx=0.03, rely=0.83, height=34, width=97)
        self.Refreshbutton.configure(activebackground="#d9d9d9")
        self.Refreshbutton.configure(activeforeground="#000000")
        self.Refreshbutton.configure(background="#d9d9d9")
        self.Refreshbutton.configure(disabledforeground="#a3a3a3")
        self.Refreshbutton.configure(foreground="#000000")
        self.Refreshbutton.configure(highlightbackground="#d9d9d9")
        self.Refreshbutton.configure(highlightcolor="black")
        self.Refreshbutton.configure(pady="0")
        self.Refreshbutton.configure(text='''Refresh''')
        self.Refreshbutton.configure(command=self.command_refresh)

        self.Label4 = Label(top)#text
        self.Label4.place(relx=0.52, rely=0.84, height=21, width=114)
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Connected to:''')
        self.Label4.configure(width=114)

        self.Serveriptext = Text(top)#outputs ip of the server
        self.Serveriptext.place(relx=0.71, rely=0.84, relheight=0.07, relwidth=0.26)
        self.Serveriptext.configure(background="#d9d9d9")
        self.Serveriptext.configure(font="TkTextFont")
        self.Serveriptext.configure(foreground="black")
        self.Serveriptext.configure(highlightbackground="#d9d9d9")
        self.Serveriptext.configure(highlightcolor="black")
        self.Serveriptext.configure(insertbackground="black")
        self.Serveriptext.configure(relief=FLAT)
        self.Serveriptext.configure(selectbackground="#c2c2c5")
        self.Serveriptext.configure(selectforeground="black")
        self.Serveriptext.configure(width=164)
        self.Serveriptext.configure(wrap=WORD)
        self.Serveriptext.insert(END,serveriptkinter)
        self.Serveriptext.configure(state=DISABLED)

        self.Cancelbutton = Button(top)#button to be pressed for command_close
        self.Cancelbutton.place(relx=0.21, rely=0.83, height=34, width=97)
        self.Cancelbutton.configure(activebackground="#d9d9d9")
        self.Cancelbutton.configure(activeforeground="#000000")
        self.Cancelbutton.configure(background="#d9d9d9")
        self.Cancelbutton.configure(disabledforeground="#a3a3a3")
        self.Cancelbutton.configure(foreground="#000000")
        self.Cancelbutton.configure(highlightbackground="#d9d9d9")
        self.Cancelbutton.configure(highlightcolor="black")
        self.Cancelbutton.configure(pady="0")
        self.Cancelbutton.configure(text='''Cancel''')
        self.Cancelbutton.configure(command=self.command_close)


#testing area
if __name__ == '__main__':
    start_gui1()
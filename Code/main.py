import os
import wx
from sound import *

def initialize():
    # Create all the variables.
    global soundfile
    soundfile = filesound()


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control = wx.StaticBox(self)#, style=wx.TE_MULTILINE)
        initialize()

        # Setting up the menu.
        filemenu = wx.Menu()
        soundmenu = wx.Menu()
        helpmenu = wx.Menu()

        # Creating the items in the menu
        # --- File menu ---
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a file")
        menuSave = filemenu.Append(wx.ID_SAVE, "Save", "Save file")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # --- Sound menu ---
        menuRecord = soundmenu.Append(wx.ID_ANY, "&Record", "Record an audio")

        # --- Help menu ---
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") 
        menuBar.Append(soundmenu, "&Sound")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnRecord, menuRecord)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)

        self.Show(True)

    def OnOpen(self, e):
        self.dirname = '.'
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.wav", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            #self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def OnSave(self, e):
        self.dirname = '.'
        dlg = wx.FileDialog(self, "Save audio", self.dirname, "", "*.wav", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            save(self.dirname, self.filename, soundfile)

        dlg.Destroy()

    def OnAbout(self, e):
        dlg = wx.MessageDialog( self, "An attempt of doing a sheet music creator.\nVersion 0.1a\n2014\nCreate by Jose Carlos M. Aragon.\nYou can ask me on twitter: @Montagon.", "About Sheet music creator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


    def OnRecord(self, e):
        soundfile.frames = record(soundfile)

    def OnExit(self, e):
        self.Close(True)

app = wx.App(False)
frame = MainWindow(None, "Sheet music creator")
app.MainLoop()
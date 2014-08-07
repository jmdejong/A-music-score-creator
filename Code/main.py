#!/usr/bin/env python

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

        # Set events of the menubar.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnRecord, menuRecord)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)


        # Creating the toolbar
        vbox = wx.BoxSizer(wx.VERTICAL)
        mainToolbar = wx.ToolBar(self)
        toolbarOpen = mainToolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('images/open32.png'))
        toolbarRecord = mainToolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('images/record32.png'))
        toolbarSave = mainToolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap('images/save32.png'))
        mainToolbar.Realize()

        # Set events of the toolbar

        self.Bind(wx.EVT_MENU, self.OnOpen, toolbarOpen)
        self.Bind(wx.EVT_MENU, self.OnRecord, toolbarRecord)
        self.Bind(wx.EVT_MENU, self.OnSave, toolbarSave)

        vbox.Add(mainToolbar, 0, wx.EXPAND)
        self.SetSizer(vbox)

        self.Show(True)

    def OnOpen(self, e):
        self.dirname = '.'
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.wav", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            wf = wave.open(self.dirname+"/"+self.filename, 'rb')
            soundfile.channels = wf.getnchannels()
            soundfile.rate = wf.getframerate()
            soundfile.frames = wf.getnframes()
            soundfile.sample_size = wf.getsampwidth()
            wf.close()
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
        dlg = wx.MessageDialog( self, "An attempt of doing a sheet music creator.\nVersion 0.1a\n2014\nCreated by Jose Carlos M. Aragon.\nYou can contact me via twitter: @Montagon.", "About Sheet music creator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


    def OnRecord(self, e):
        soundfile.frames = record(soundfile)

    def OnExit(self, e):
        self.Close(True)

app = wx.App(False)
frame = MainWindow(None, "Sheet music creator")
app.MainLoop()
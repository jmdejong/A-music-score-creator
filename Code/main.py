#!/usr/bin/env python

import os
import wx
from sound import *

def initialize():
    # Create all the variables.
    global audioData
    audioData = AudioData()


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        initialize()
        global menuSave, menuPlay, soundfile, audioData, menuAudioProcess, sounddirectory
        #sounddirectory = "/tmp/"

        # Setting up the menu.
        filemenu = wx.Menu()
        soundmenu = wx.Menu()
        helpmenu = wx.Menu()

        # Creating the items in the menu
        # --- File menu ---
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a file")
        menuSave = filemenu.Append(wx.ID_SAVE, "Save", "Save file")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        menuSave.Enable(False)


        # --- Sound menu ---
        menuRecord = soundmenu.Append(wx.ID_ANY, "&Record", "Record an audio")
        menuPlay = soundmenu.Append(wx.ID_ANY, "Play", "Play an audio")
        menuAudioProcess = soundmenu.Append(wx.ID_ANY, "Generate PDF", "Generate PDF from audio")
        menuPlay.Enable(False)
        menuAudioProcess.Enable(False)

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
        self.Bind(wx.EVT_MENU, self.OnPlay, menuPlay)
        self.Bind(wx.EVT_MENU, self.OnAudioProcess, menuAudioProcess)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)


        # Creating the toolbar
        vbox = wx.BoxSizer(wx.VERTICAL)
        global mainToolbar
        mainToolbar = wx.ToolBar(self)
        toolbarOpen = mainToolbar.AddLabelTool(wx.ID_OPEN, '', wx.Bitmap('images/open32.png'))
        toolbarSave = mainToolbar.AddLabelTool(wx.ID_SAVE, '', wx.Bitmap('images/save32.png'))
        mainToolbar.AddSeparator()
        toolbarRecord = mainToolbar.AddLabelTool(5990, '', wx.Bitmap('images/record32.png'))
        toolbarPlay = mainToolbar.AddLabelTool(6001, '', wx.Bitmap('images/play32.png'))
        toolbarAudioProcess = mainToolbar.AddLabelTool(6002, '', wx.Bitmap('images/pdf32.png'))
        mainToolbar.EnableTool(wx.ID_SAVE, False) # Before we have an audio, it's deactivated.
        mainToolbar.EnableTool(6001, False)
        mainToolbar.EnableTool(6002, False)
        mainToolbar.Realize()

        # Set events of the toolbar

        self.Bind(wx.EVT_MENU, self.OnOpen, toolbarOpen)
        self.Bind(wx.EVT_MENU, self.OnRecord, toolbarRecord)
        self.Bind(wx.EVT_MENU, self.OnPlay, toolbarPlay)
        self.Bind(wx.EVT_MENU, self.OnAudioProcess, toolbarAudioProcess)
        self.Bind(wx.EVT_MENU, self.OnSave, toolbarSave)

        vbox.Add(mainToolbar, 0, wx.EXPAND)
        self.SetSizer(vbox)

        self.Show(True)

    def OnOpen(self, e):
        global soundfile, audioData, sounddirectory
        self.dirname = '.'
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.wav", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            sounddirectory = self.dirname+"/"+self.filename
            soundfile = wave.open(self.dirname+"/"+self.filename, 'rb')
            mainToolbar.EnableTool(wx.ID_SAVE, True)
            mainToolbar.EnableTool(6001, True)
            mainToolbar.EnableTool(6002, True)
            menuSave.Enable(True)
            menuPlay.Enable(True)
            menuAudioProcess.Enable(True) 
            
        dlg.Destroy()

    def OnRecord(self, e):
        global soundfile,menuSave, menuPlay, menuAudioProcess, audioData, sounddirectory
        mainToolbar.EnableTool(5990, False)
        (soundfile, frames, sounddirectory) = record(audioData)
        audioData.frames = frames
        mainToolbar.EnableTool(5990, True)
        mainToolbar.EnableTool(wx.ID_SAVE, True)
        mainToolbar.EnableTool(6001, True)
        mainToolbar.EnableTool(6002, True)
        menuSave.Enable(True)
        menuPlay.Enable(True)
        menuAudioProcess.Enable(True)

    def OnAudioProcess(self, e):
        #Add interaction to save the file. In test, only the path to the file to process
        global sounddirectory
        audioProcessing(sounddirectory)

    def OnSave(self, e):
        global soundfile, audioData
        self.dirname = '.'
        dlg = wx.FileDialog(self, "Save audio", self.dirname, "", "*.wav", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            save(self.dirname, self.filename, soundfile, audioData)
        dlg.Destroy()

    def OnAbout(self, e):
        dlg = wx.MessageDialog( self, "An attempt of doing a sheet music creator.\nVersion 0.2a\n2014\nCreated by Jose Carlos M. Aragon.\nYou can contact me via twitter: @Montagon.", "About Sheet music creator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPlay(self, e):
        global soundfile, audioData, sounddirectory
        print(sounddirectory)
        play(soundfile, audioData, sounddirectory)

    def OnExit(self, e):
        self.Close(True)

app = wx.App(False)
frame = MainWindow(None, "Sheet music creator")
app.MainLoop()
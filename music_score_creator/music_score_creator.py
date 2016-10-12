#!/usr/bin/env python

    # <Music score creator. Generate a sheet music from an audio.>
    # Copyright (C) <2014>  <Jose Carlos Montanez Aragon>
    # Modified by Troido

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

import os
import wx
import time
import sound
import wave
import pygame



class MainWindow():
    def __init__(self, parent, title):
        self.frame = wx.Frame(parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, title=title, size=(300,350))
        # WHY FUCKING GLOBALS? GLOBALS VARIABLES ARE EVIL!
        global menuSave, menuPlay, soundfile, audioData, menuAudioProcess
        global sounddirectory, tRecord, tTunning, menuPlayMidi
        audioData = sound.AudioData()
        panel = wx.Panel(self.frame)

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
        menuPlayMidi = soundmenu.Append(wx.ID_ANY, "Play MIDI", "Play MIDI")
        menuPlay.Enable(False)
        menuAudioProcess.Enable(False)
        menuPlayMidi.Enable(False)

        # --- Help menu ---
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") 
        menuBar.Append(soundmenu, "&Sound")
        menuBar.Append(helpmenu, "&Help")
        self.frame.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events of the menubar.
        self.frame.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
        self.frame.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.frame.Bind(wx.EVT_MENU, self.onRecord, menuRecord)
        self.frame.Bind(wx.EVT_MENU, self.onPlay, menuPlay)
        self.frame.Bind(wx.EVT_MENU, self.onAudioProcess, menuAudioProcess)
        self.frame.Bind(wx.EVT_MENU, self.onOpen, menuOpen)
        self.frame.Bind(wx.EVT_MENU, self.onSave, menuSave)
        self.frame.Bind(wx.EVT_MENU, self.onPlayMidi, menuPlayMidi)


        # Creating the toolbar
        vbox = wx.BoxSizer(wx.VERTICAL)
        global mainToolbar
        mainToolbar = wx.ToolBar(self.frame)
        toolbarOpen = mainToolbar.AddLabelTool(wx.ID_OPEN, '', wx.Bitmap('images/open32.png'))
        toolbarSave = mainToolbar.AddLabelTool(wx.ID_SAVE, '', wx.Bitmap('images/save32.png'))
        mainToolbar.AddSeparator()
        toolbarRecord = mainToolbar.AddLabelTool(5990, '', wx.Bitmap('images/record32.png'))
        toolbarPlay = mainToolbar.AddLabelTool(6001, '', wx.Bitmap('images/play32.png'))
        mainToolbar.AddSeparator()
        toolbarAudioProcess = mainToolbar.AddLabelTool(6002, '', wx.Bitmap('images/pdf32.png'))
        toolbarPlayMidi = mainToolbar.AddLabelTool(6003, '', wx.Bitmap('images/play32.png'))
        mainToolbar.EnableTool(wx.ID_SAVE, False) # Before we have an audio, it's deactivated.
        mainToolbar.EnableTool(6001, False)
        mainToolbar.EnableTool(6002, False)
        mainToolbar.EnableTool(6003, False)
        mainToolbar.Realize()

        # Set events of the toolbar

        self.frame.Bind(wx.EVT_MENU, self.onOpen, toolbarOpen)
        self.frame.Bind(wx.EVT_MENU, self.onRecord, toolbarRecord)
        self.frame.Bind(wx.EVT_MENU, self.onPlay, toolbarPlay)
        self.frame.Bind(wx.EVT_MENU, self.onAudioProcess, toolbarAudioProcess)
        self.frame.Bind(wx.EVT_MENU, self.onSave, toolbarSave)
        self.frame.Bind(wx.EVT_MENU, self.onPlayMidi, toolbarPlayMidi)

        vbox.Add(mainToolbar, 0, wx.EXPAND)

        # 

        instruments = ["Piano", "Clarinet", "Flute", "Trumpet", "Alto Saxo"]
        wx.StaticText(self.frame, label=("Instrument"), pos=(10, 74))
        cb_instrument = wx.ComboBox(self.frame, value=("Piano"), pos=(169, 70), size=(120, 28), choices=instruments, style=wx.CB_READONLY)

        tempos = ['60', '90', '120', '150']
        wx.StaticText(self.frame, label=("Tempo"), pos=(10, 114))
        cb_tempo = wx.ComboBox(self.frame, value=('60'), pos=(209, 110), size=(80, 28), choices=tempos, 
            style=wx.CB_READONLY)

        wx.StaticLine(self.frame, pos=(0, 50), size=(300,1))

        tRecord = wx.TextCtrl(self.frame,-1, pos=(209, 150), value="2")
        wx.StaticText(self.frame, label=("Recording time (seconds)"), pos=(10, 154))
        #wx.StaticText(self.frame, label=("seconds"), pos=(210, 114))

        measures = ['2/4', '3/4', '4/4']
        wx.StaticText(self.frame, label=("Measure"), pos=(10, 194))
        cb_measure = wx.ComboBox(self.frame, value=('4/4'), pos=(209, 190), size=(80, 28), choices=measures, 
            style=wx.CB_READONLY)

        tTunning = wx.TextCtrl(self.frame, -1, pos=(209, 230), value="440")
        wx.StaticText(self.frame, label=("Tuning"), pos=(10, 234))

        notes = ['Semibreve', 'Minim', 'Crotchet', 'Quaver', 'Semiquaver']
        tMinimumNote = wx.StaticText(self.frame, label=("Minimum note"), pos=(10, 274))
        cb_minimumNote = wx.ComboBox(self.frame, value=('Semiquaver'), pos=(159, 270), size=(130, 28), choices=notes)

        cb_midi = wx.CheckBox(self.frame, label="Generate MIDI", pos=(10, 314))


        # Events of the block

        self.frame.Bind(wx.EVT_COMBOBOX, self.onTempo, cb_tempo)
        self.frame.Bind(wx.EVT_COMBOBOX, self.onMeasure, cb_measure)
        self.frame.Bind(wx.EVT_CHECKBOX, self.onMidi, cb_midi)
        self.frame.Bind(wx.EVT_COMBOBOX, self.onInstrument, cb_instrument)
        self.frame.Bind(wx.EVT_COMBOBOX, self.onMinimumNote, cb_minimumNote)

        self.frame.SetSizer(vbox)

        self.frame.Show(True)

    def onOpen(self, e):
        global soundfile, audioData, sounddirectory
        dlg = wx.FileDialog(self.frame, "Choose a file", '.', "", "*.wav", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            sounddirectory = dlg.getPath()
            soundfile = wave.open(dlg.getPath(), 'rb')
            mainToolbar.EnableTool(wx.ID_SAVE, True)
            mainToolbar.EnableTool(6001, True)
            mainToolbar.EnableTool(6002, True)
            menuSave.Enable(True)
            menuPlay.Enable(True)
            menuAudioProcess.Enable(True) 
            
        dlg.Destroy()

    def onRecord(self, e):
        global soundfile,menuSave, menuPlay, menuAudioProcess, audioData, sounddirectory
        global tRecord
        mainToolbar.EnableTool(5990, False)
        audioData.record_seconds = int(tRecord.GetValue())
        (soundfile, frames, sounddirectory) = sound.record(audioData)
        audioData.frames = frames
        mainToolbar.EnableTool(5990, True)
        mainToolbar.EnableTool(wx.ID_SAVE, True)
        mainToolbar.EnableTool(6001, True)
        mainToolbar.EnableTool(6002, True)
        menuSave.Enable(True)
        menuPlay.Enable(True)
        menuAudioProcess.Enable(True)

    def onAudioProcess(self, e):
        #Add interaction to save the file. In test, only the path to the file to process
        global sounddirectory, tTunning, audioData, menuPlayMidi
        audioData = sound.updateConversionList(audioData, int(tTunning.GetValue()))
        sound.audioProcessing(sounddirectory, audioData)
        if audioData.midi == 1:
            mainToolbar.EnableTool(6003, True)
            menuPlayMidi.Enable(True)
        if audioData.midi == 0:
            mainToolbar.EnableTool(6003, False)
            menuPlayMidi.Enable(False)

    def onSave(self, e):
        global soundfile, audioData
        dlg = wx.FileDialog(self.frame, "Save audio", '.', "", "*.wav", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            sound.save(dirname, filename, audioData)
        dlg.Destroy()

    def onAbout(self, e):
        dlg = wx.MessageDialog( self.frame, "An attempt of doing a music score creator.\nVersion 0.9beta - 2014\nCreated by Jose Carlos M. Aragon.\nModified by Troido.\n", "About Music score creator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onPlay(self, e):
        global soundfile, audioData, sounddirectory
        sound.play(sounddirectory, audioData)

    def onExit(self, e):
        self.frame.Close(True)

    def onTempo(self, e):
        global audioData
        audioData.quarter_note_minute = int(e.GetString())

    def onMeasure(self, e):
        global audioData
        audioData.measure = e.GetString()

    def onMidi(self, e):
        global audioData
        sender = e.GetEventObject()
        isChecked = sender.GetValue()

        if isChecked:
            audioData.midi = 1
        else:
            audioData.midi = 0

    def onPlayMidi(self, e):
        global audioData
        pygame.mixer.init(audioData.rate, audioData.format, audioData.channels, audioData.chunk)
        pygame.mixer.music.load("score.midi")
        pygame.mixer.music.play()

    def onInstrument(self, e):
        global audioData
        audioData.instrument = e.GetString()

    def onMinimumNote(self, e):
        global audioData
        note_conversion =  {"Semibreve": 16,
                            "Minim": 8,
                            "Crotchet": 4,
                            "Quaver": 2,
                            "Semiquaver": 1}
        audioData.minimum_note = note_conversion[e.GetString()]


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, "Music score creator")
    app.MainLoop()
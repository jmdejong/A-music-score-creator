
import pyaudio

# Class that stores values for the proper treatment of time,
# recording settings and more.
class AudioData():
    def __init__(self):
        self.channels = 1
        self.format = pyaudio.paInt16
        self.rate = 8000
        self.frames = 0
        self.chunk = 2000
        self.record_seconds = 1
        self.sample_size = 0
        self.quarter_note_minute = 60 
        self.measure = '4/4'
        self.isMidi = False
        self.instrument = "Piano"
        self.minimum_note = 1
    
    
    

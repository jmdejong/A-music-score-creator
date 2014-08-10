import pyaudio
import wave
import time

# Experimental, to do the fft and some test

from pylab import*
from scipy.io import wavfile

# End experimental

def audioProcessing(filename):
	sampFreq, snd = wavfile.read(filename)
	print(sampFreq)

class AudioData():
	def __init__(self):
		self.channels = 1
		self.format = pyaudio.paInt16
		self.rate = 8000
		self.frames = 0
		self.chunk = 1024
		self.record_seconds = 2
		self.sample_size = 0

def record(audioData):
	global sounddirectory
	p = pyaudio.PyAudio()

	stream = p.open(format=audioData.format,
	                channels=audioData.channels,
	                rate=audioData.rate,
	                input=True,
	                frames_per_buffer=audioData.chunk) #buffer

	print("* recording")

	frames = []

	for i in range(0, int(audioData.rate / audioData.chunk * audioData.record_seconds)):
	    data = stream.read(audioData.chunk)
	    frames.append(data) # 2 bytes(16 bits) per channel

	print("* done recording")

	audioData.sample_size = p.get_sample_size(audioData.format)
	stream.stop_stream()
	sounddirectory = "/tmp/"+time.strftime("%H%M%S")+".wav"

	wf = wave.open(sounddirectory, 'wb')
	wf.setnchannels(audioData.channels)
	wf.setsampwidth(p.get_sample_size(audioData.format))
	audioData.sample_size = p.get_sample_size(audioData.format)
	wf.setframerate(audioData.rate)
	wf.writeframes(b''.join(frames))
	wf.close()

	stream.close()
	p.terminate()
	return (stream, frames, sounddirectory)

def save(dirname, filename, soundfile, audioData):
	wf = wave.open(dirname+"/"+filename+".wav", 'wb')
	wf.setnchannels(audioData.channels)
	wf.setsampwidth(audioData.sample_size)
	wf.setframerate(audioData.rate)
	wf.writeframes(b''.join(audioData.frames))
	wf.close()

def play(soundfile, aData, sounddirectory):

	f = wave.open(sounddirectory,"rb")  
	p = pyaudio.PyAudio()  

	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
	                channels = f.getnchannels(),  
	                rate = f.getframerate(),  
	                output = True)  
	data = f.readframes(aData.chunk)  

	while data != '':  
	    stream.write(data)  
	    data = f.readframes(aData.chunk)  
  
	stream.stop_stream()  
	stream.close()   
	p.terminate()  

import os
import pyaudio
import wave
import time
from pylab import*
from scipy.io import wavfile
import numpy

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
		self.measure = '3/4'

conversion = [(10000.0,1077.0,"r"),
			  (1077.0,1017.1,"c''"),
			  (1017.0,960.0,"b''"),	
			  (960.0,906.2,"ais''"),
			  (906.2,855.3,"a''"),
			  (855.3,807.3,"gis''"),
			  (807.3,762.0,"g''"),
			  (762.0,719.2,"fis''"),
			  (719.2,678.9,"f''"),
			  (678.9,640.8,"e''"),
			  (640.8,604.8,"dis''"),
			  (604.8,570.8,"d''"),
			  (570.8,538.8,"cis''"),
			  (538.8,508.6,"c''"),
			  (508.6,480.0,"b'"),
			  (480.0,453.1,"ais'"),
			  (453.1,427.7,"a'"),
			  (427.7,403.6,"gis'"),
			  (403.6,381.0,"g'"),
			  (381.0,359.6,"fis'"),
			  (359.6,339.4,"f'"),
			  (339.4,320.4,"e'"),
			  (320.4,302.4,"dis'"),
			  (302.4,285.4,"d'"),
			  (285.4,269.4,"cis'"),
			  (269.4,254.3,"c'"),
			  (254.3,240.0,"b"),
			  (240.0,226.5,"ais"),
			  (226.5,213.8,"a"),
			  (213.8,201.8,"gis"),
			  (201.8,190.5,"g"),
			  (190.5,179.8,"fis"),
			  (179.8,169.7,"f"),
			  (169.7,160.2,"e"),
			  (160.2,0.0,"r")]


def tempo(audioData):
	quarter_note = audioData.quarter_note_minute/60.0 # 
	semiquaver = 4*quarter_note

	# Determining the size of the chunk. That is, the number of semiquaver for second
	audioData.chunk = int(ceil(2530 - 200*semiquaver))

	return audioData



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

def audioProcessing(filename, audioData):
	list_of_freq = getListofFreq(filename, audioData)
	final_list = preprocessingFreqs(list_of_freq, audioData)
	writeFile(final_list)
	os.system("lilypond -s score.ly")


def getListofFreq(filename, audioData):
	wf = wave.open(filename, 'rb')
	swidth = wf.getsampwidth()
	RATE = wf.getframerate()
	audioData = tempo(audioData)

	# Use a Blackman window
	window = numpy.blackman(audioData.chunk)

	# Read some data
	data = wf.readframes(audioData.chunk)
	# Find the frequency of each chunk
	list_of_freq = []
	while len(data) == audioData.chunk*swidth:

	    # Unpack the data and times by the hamming window
	    indata = numpy.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
	                                         data))*window
	    # Take the fft and square each value
	    fftData=abs(numpy.fft.rfft(indata))**2
	    # Find the maximum
	    which = fftData[1:].argmax() + 1
	    # Use quadratic interpolation around the max
	    if which != len(fftData)-1:
	        y0,y1,y2 = numpy.log(fftData[which-1:which+2:])
	        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
	        # Find the frequency and output it
	        thefreq = (which+x1)*RATE/audioData.chunk
#	        print "The freq is %f Hz." % (thefreq)
	        list_of_freq.append(thefreq)
	    else:
	        thefreq = which*RATE/audioData.chunk
#	        print "The freq is %f Hz." % (thefreq)
	        list_of_freq.append(thefreq)
	    # Read some more data
	    data = wf.readframes(audioData.chunk)


	return list_of_freq

def preprocessingFreqs(list_of_freq, audioData):

	list_ = []
	for i in list_of_freq:
		for j in conversion:
			if j[1] < i <= j[0]:
				list_.append(j[2])

	
	n = 0
	if audioData.measure == '2/4':
		n = 8
	if audioData.measure == '3/4':
		n = 12
	if audioData.measure == '4/4':
		n = 16

	final_list = []
	j = 0
	for m in range(len(list_)/n + 1):
		note = list_[j] 
		cont = 16
		for i in range(1,n):
			if j+i <= len(list_)-1:
				if list_[j+i] == note:
					cont = cont / 2
				else:
					final_list.append(note + str(cont/2))
					cont = 16
					note = list_[j+i]
					if i+j+1 == len(list_):
						final_list.append(note + str(cont/2))
		
		j = j + n

	return final_list

def writeFile(final_list):
	f = open('score.ly', "w")

	f.write("\score {\n\t\\version \"2.16.2\"{\n\t\t\\time 4/4\n\t\t\key c \major\n\t\t")
	for i in (final_list):
		f.write(i)
		f.write(" ")
	f.write("\n\t}\n}\n")
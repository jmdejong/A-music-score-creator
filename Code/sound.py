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
		self.quarter_note_minute = 60 # Allowed values: 60, 90, 120
		self.measure = '3/4'


def tempo(audioData):
	#global audioData
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
	        print "The freq is %f Hz." % (thefreq)
	        list_of_freq.append(thefreq)
	    else:
	        thefreq = which*RATE/audioData.chunk
	        print "The freq is %f Hz." % (thefreq)
	        list_of_freq.append(thefreq)
	    # Read some more data
	    data = wf.readframes(audioData.chunk)


	return list_of_freq

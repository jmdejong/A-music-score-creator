import pyaudio
import wave

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
	#stream.close()
	p.terminate()
	return (stream, frames)

def save(dirname, filename, soundfile, audioData):
	wf = wave.open(dirname+"/"+filename+".wav", 'wb')
	wf.setnchannels(audioData.channels)
	wf.setsampwidth(soundfile.get_sample_size(audioData.format))
	wf.setframerate(audioData.rate)
	wf.writeframes(b''.join(audioData.frames))
	wf.close()

def play(soundfile, aData):

	#f = wave.open(r"/usr/share/sounds/alsa/Rear_Center.wav","rb")  
	#instantiate PyAudio  
	p = pyaudio.PyAudio()  
	#open stream  
	stream = p.open(format = p.get_format_from_width(soundfile.getsampwidth()),  
	                channels = soundfile.getnchannels(),  
	                rate = soundfile.getframerate(),  
	                output = True)  
	#read data  
	data = soundfile.readframes(aData.chunk)  

	#paly stream  
	while data != '':  
	    stream.write(data)  
	    data = soundfile.readframes(aData.chunk)  

	#stop stream  
	stream.stop_stream()  
	stream.close()  

	#close PyAudio  
	#p.terminate()  

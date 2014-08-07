import pyaudio
import wave


class filesound():
	def __init__(self):
		self.channels = 1
		self.format = pyaudio.paInt16
		self.rate = 8000
		self.frames = 0
		self.chunk = 1024
		self.record_seconds = 1
		self.sample_size = 0


def record(soundfile):
	#CHUNK = 1024 
	#FORMAT = pyaudio.paInt16 #paInt8
	#CHANNELS = 1 
	#RATE = 44100 #sample rate
	#RECORD_SECONDS = 2
	#WAVE_OUTPUT_FILENAME = "output.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=soundfile.format,
	                channels=soundfile.channels,
	                rate=soundfile.rate,
	                input=True,
	                frames_per_buffer=soundfile.chunk) #buffer

	print("* recording")

	frames = []

	for i in range(0, int(soundfile.rate / soundfile.chunk * soundfile.record_seconds)):
	    data = stream.read(soundfile.chunk)
	    frames.append(data) # 2 bytes(16 bits) per channel

	print("* done recording")

	soundfile.sample_size = p.get_sample_size(soundfile.format)
	stream.stop_stream()
	stream.close()
	p.terminate()
	return frames

def save(dirname, filename, soundfile):
	wf = wave.open(dirname+"/"+filename+".wav", 'wb')
	wf.setnchannels(soundfile.channels)
	wf.setsampwidth(soundfile.sample_size)
	wf.setframerate(soundfile.rate)
	wf.writeframes(b''.join(soundfile.frames))
	wf.close()

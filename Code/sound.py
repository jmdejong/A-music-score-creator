import pyaudio
import wave


class filesound():
	def __init__(self):
		self.channels = 1
		self.format = pyaudio.paInt16
		self.rate = 44100
		self.frames = 0


def record():
	CHUNK = 1024 
	FORMAT = pyaudio.paInt16 #paInt8
	CHANNELS = 1 
	RATE = 44100 #sample rate
	RECORD_SECONDS = 2
	WAVE_OUTPUT_FILENAME = "output.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK) #buffer

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data) # 2 bytes(16 bits) per channel

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()
	return frames
	#wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	#wf.setnchannels(CHANNELS)
	#wf.setsampwidth(p.get_sample_size(FORMAT))
	#wf.setframerate(RATE)
	#wf.writeframes(b''.join(frames))
	#wf.close()

def save(name, file):
	pass

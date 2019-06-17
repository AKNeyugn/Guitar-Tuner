import pyaudio
import wave


# parametres du flux audio
CHUNK = 1024 #nombre de points d'echantillonage
FORMAT = pyaudio.paInt16 #16 bit
CHANNELS = 1 #mono
RATE = 44100 #frequence d'echantillonage


RECORD_SECONDS = 5
filename = "Test.wav"

# intialiser PyAudio
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# enregistrement
print("* recording")

frames = []

for i in range(0, int(RATE * RECORD_SECONDS), int(CHUNK)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

# 'ecrire' les donnees enregistrees sur un fichier WAV
wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


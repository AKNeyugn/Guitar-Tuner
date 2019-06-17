import pyaudio  
import wave  

chunk = 1024  

#open a wav format music  
f = wave.open("ShortTest.wav")  

#instantiate PyAudio  
p = pyaudio.PyAudio()  

#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True) 
 
#set variables
length = f.getnframes()
print(length)
  
parametres = f.getsampwidth()
parametre = f.getframerate()
print(parametres)
print(parametre)

data = f.readframes(chunk)

#play stream until a given time
while len(data) > 0:  
    stream.write(data)  
    data = f.readframes(chunk)
   
#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()  


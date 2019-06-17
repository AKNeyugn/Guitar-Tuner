from scipy.io import wavfile
from scipy.fftpack import fft
import numpy
import wave

#read data from wave file
def frequence(wf):
    rate, data = wavfile.read(wf); # 2D array of sampling rate and values
    print(data)
    a = fft(data)
    n = data.size;
    print(n)
    #print(len(data))
    #print(rate)
    timestep = 1/rate; 
    freqs = numpy.fft.fftfreq(n, d=timestep)
    idx = numpy.argmax(numpy.abs(a))
    freq = freqs[idx]
    print(freqs)
    #freq_in_hertz = abs(freq * int(frate))
    print(int(freq))
    #print(freq_in_hertz)

frequence("1_Mi3.wav")
frequence("2_Si2.wav")
frequence("3_Sol2.wav")
frequence("4_Re2.wav")
frequence("5_La1.wav")
frequence("6_Mi1.wav")


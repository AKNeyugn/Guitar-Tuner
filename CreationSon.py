import math
import wave
import struct

# Fonction pour créer un son de reference
def SonRef(f,filename):
    freq = int(f)   #La fréquence du son
    data_size = RATE * RECORD_SECONDS
    amplitude = 64000.0     
    fname = str(filename) + ".wav"

    # On définit 
    sine_list_x = []
    for x in range(data_size):
        sine_list_x.append(math.sin(2*math.pi*freq*(x/RATE)))
    
    wf = wave.open(fname, "w")

    #Les paramètres du fichier WAV
    nchannels = CHANNELS
    sampwidth = 2
    framerate = int(RATE)
    nframes = data_size
    comptype = "NONE"
    compname = "not compressed"

    wf.setparams((nchannels, sampwidth, framerate, nframes,
        comptype, compname))

    #
    for s in sine_list_x:
        wf.writeframes(struct.pack('h', int(s*amplitude/2)))

    wf.close()

SonRef(82,"6_E2")
SonRef(110,"5_A2")
SonRef(147,"4_D3")
SonRef(196,"3_G3")
SonRef(247,"2_B3")
SonRef(330,"1_E4")
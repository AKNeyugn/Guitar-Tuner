import wave

# Paramètres nécéssaires pour manipulation audio
CHUNK = 1024    # nombre de points d'échantillonage
CHANNELS = 1    # mono
RATE = 44100    # fréquence d'échantillonage
RECORD_SECONDS = 4  # durée d'un fichier

# Fonction pour couper premiere seconde d'un fichier audio
def Shorten(filename):
    #print("* Loading")

    fname = str(filename) + ".wav"
    wf = wave.open(fname, "r")

    nchannels = CHANNELS
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    fpms = int(framerate)# frames per ms
    nframes = (3  - 1) * fpms
    comptype = "NONE"
    compname = "not compressed"
    start_index = 1 * fpms

    newfile = wave.open("Short" + fname, "w")
    newfile.setparams((nchannels, sampwidth, framerate, nframes,
        comptype, compname))
    
    wf.rewind()
    anchor = wf.tell()
    wf.setpos(anchor + start_index)
    newfile.writeframes(wf.readframes(nframes))

    #print("* Done")

Shorten("Test")
import pyaudio
import wave
import numpy
import math
import struct
from scipy.io import wavfile
from scipy.fftpack import fft
from tkinter import *

# Paramètres nécéssaires pour manipulation audio
CHUNK = 1024    # nombre de points d'échantillonage
FORMAT = pyaudio.paInt16    # codage en 16 bit
CHANNELS = 1    # mono
RATE = 44100    # fréquence d'échantillonage
RECORD_SECONDS = 4  # durée d'un fichier

"""---------------------------------------------------------------------"""
# Fonction pour enregistrer audio
def Enregistrer(filename):
    fname = str(filename) + ".wav"
    
    # intialiser PyAudio
    p = pyaudio.PyAudio()

    # ouvrir le flux audio (les paramètres)
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=int(RATE),
                    input=True,
                    frames_per_buffer=CHUNK)

    # enregistrement
    print("* Enregistrement")

    frames = []

    for i in range(0, int(RATE * RECORD_SECONDS), int(CHUNK)):
        data = stream.read(CHUNK)   # On lit les données du flux audio
        frames.append(data)     # On ajoute les donnés lues dans une liste

    print("* Enregistrement fini")

    # fermer le flux audio et PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 'écrire' les données enregistrées sur un fichier WAV
    wf = wave.open(fname, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Fonction pour jouer audio
def Jouer(filename):
    # ouvrir un fichier wav
    wf = wave.open(str(filename) + ".wav")  

    # intialiser PyAudio  
    p = pyaudio.PyAudio()  

    # ouvrir le flux audio (les paramètres)
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=int(RATE),
                    output=True)

    # jouer le flux audio
    print("* Lecture du son")

    data = wf.readframes(CHUNK) # On lit les données du fichier WAV

    while len(data) > 0:  
        stream.write(data)  # On 'écrit' ces données dans le flux audio
        data = wf.readframes(CHUNK)

    print("* Lecture finie")
    
    # fermer le flux audio et PyAudio
    stream.stop_stream()  
    stream.close()  
    p.terminate() 

# Fonction pour couper 1s au début et à la fin d'un fichier audio
def Raccourcir(filename):
    fname = str(filename) + ".wav"
    wf = wave.open(fname, "r")

    # Les paramètres du nouveau fichier
    nchannels = CHANNELS
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    nframes = framerate * (3 - 1)   # La taille du nouveau fichier, en coupant 1s au début et à la fin
    comptype = "NONE"
    compname = "not compressed"

    start_index = 1 * framerate     # On définit le début du fichier WAV

    newfile = wave.open("Rac" + fname, "w")
    newfile.setparams((nchannels, sampwidth, framerate, nframes,
        comptype, compname))
    
    wf.rewind()     # On repositionne le curseur à la position 0
    anchor = wf.tell()      # La position du curseur dans le fichier WAV
    wf.setpos(anchor + start_index)     # On positionne le curseur

    # 'écrire' les données dans le fichier raccourci
    newfile.writeframes(wf.readframes(nframes))

# Fonction pour créer un son de reference
def SonRef(f,filename):
    freq = int(f)   # La fréquence du son
    data_size = RATE * RECORD_SECONDS
    amplitude = 64000.0     
    fname = str(filename) + ".wav"

    # On crée un tableau de valeur de la fonction périodique du son
    sine_list_x = []
    for x in range(data_size):
        sine_list_x.append(math.sin(2*math.pi*freq*(x/RATE)))
    
    wf = wave.open(fname, "w")

    # Les paramètres du fichier WAV
    nchannels = CHANNELS
    sampwidth = 2
    framerate = int(RATE)
    nframes = data_size
    comptype = "NONE"
    compname = "not compressed"

    wf.setparams((nchannels, sampwidth, framerate, nframes,
        comptype, compname))

    # 'écrire' les données en bit à partir du tableau de valeur
    for s in sine_list_x:
        wf.writeframes(struct.pack('h', int(s*amplitude/2)))

    wf.close()

# Fonction pour analyse audio/donner la fréquence du son d'un fichier wav
def Frequence(filename):

    fname = str(filename) + ".wav"
    rate, data = wavfile.read(fname)    # On obtient ici un tableau à 2 dimensions
    a = fft(data)   # Analyse de Fourrier FFT
    n = data.size
    timestep = 1/rate
    freqs = numpy.fft.fftfreq(n, d=timestep)    # On obtient ici une liste des fréquences (harmoniques)
    idx = numpy.argmax(numpy.abs(a))
    freq = freqs[idx]   # La fréquence du son qu'on cherche

    return int(freq)

# Fonction pour comparer deux fréquences
def Comparer(f,fref):
    if f < int(fref-5):
        return "inf"
    elif f > int(fref+5):
        return "sup"
    elif f <= int(fref+5) and f >= int(fref-5):
        return "egal"

# Fonction pour suggestion 
def Suggestion(resultat):
    if resultat == "inf":
        print("Déserrez la clef")
    elif resultat == "sup":
        print("Serrez la clef")
    elif resultat == "egal":
        print("Votre corde est bien accordée!")

"""---------------------------------------------------------------------"""
# Créer les fichiers sons de référence
"""SonRef(82,"6_E2")
SonRef(110,"5_A2")
SonRef(147,"4_D3")
SonRef(196,"3_G3")
SonRef(247,"2_B3")
SonRef(330,"1_E4")"""

Freq = ["1_E4", "2_B3", "3_G3", "4_D3", "5_A2", "6_E2"]

choix = str(input("Quelle demo? Accordage (1) ou Enregistrement puis Lecture (2)?"))
print("")

if choix == str(1):     # Un exemple d'accordage
    print("Quelle corde?")
    n = input()

    #Enregistrer("Corde" + str(n))
    print("")
    print("Corde n" + str(n))
    fref = Frequence(str(Freq[int(n)-1]))
    Raccourcir("Corde" + str(n))
    f = Frequence("RacCorde" + str(n))

    print("fref = " + str(fref) + " Hz")
    print("f = " + str(f) + " Hz")

    resultat = Comparer(f, fref)
    Suggestion(resultat)
elif choix == str(2):       # Un exemple d'enregistrement puis lecture
    Enregistrer("CordeTest")
    print("")
    Jouer("CordeTest")
else:
    print("Erreur")



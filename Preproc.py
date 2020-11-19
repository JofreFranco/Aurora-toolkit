'''
Convoluciona grabaciones de sine sweep con un filtro inverso. Si dentro de un mismo archivo hay mas de una medición los recorta

- Cargar un filtro inverso
- Cargar el directorio donde estan los audios a convolucionar
- Se convolucionan todos los archivos .wav del directorio que se cargo con el filtro inverso
- Se crea una Carpeta RIRs en el directorio
- Se guarda cada uno de los archivos convolucionados con el mismo nombre que tenia el archivo original pero finalizado en "n_RIR"
'''


import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from scipy.io import wavfile
from scipy import signal
from tqdm import tqdm
import soundfile as sf

root = tk.Tk()
root.withdraw()

filename = filedialog.askopenfilename(title = "Cargar filtro inverso") #Cargar el filtro inverso
initialdirectory = os.path.dirname(filename) 
filtroinverso,fs = sf.read(filename)
silence_duration = int(input('Duración del silencio:'))
sweep_duration = int(input('Duración del Sinesweep'))

Directorio = filedialog.askdirectory(initialdir = initialdirectory ,title = "Directorio de los archivos para convolucionar"); #Carga el directorio de los audios a convolucionar
try:
	os.mkdir(Directorio+'/RIRs')
except:
	print('El directorio RIRs ya existe')

sumfil = sum(filtroinverso)

for entry in tqdm(os.listdir(Directorio)): #Lista todo lo que este en el directorio. El tqdm es la barra de estado, asi como esta la barra de estado cuenta todos los archivos que haya en la carpeta, no solo los audios, tengo que ver como corregirlo.
	if os.path.isfile(os.path.join(Directorio,entry)) and os.path.splitext(entry)[1]==".wav": #Si el elemento de la lista es un archivo (o sea no una carpeta) y ademas es .wav sigue
		name = os.path.splitext(entry)[0]
		Data, fs2 = sf.read(Directorio + "/" + entry)
		N_med = np.int(len(Data)/((int(silence_duration)+int(sweep_duration))*fs2))
		for n in range(N_med):
			#Data=Data[0][:]
			#print(size(Data))
			if fs2 == fs:

				impulso = signal.convolve(Data[n*((silence_duration+sweep_duration)*fs2):(n*((silence_duration+sweep_duration)*fs2))+((silence_duration+sweep_duration)*fs2)],filtroinverso,mode = 'same') / sumfil  #Convoluciona el audio con el filtro inverso
				inicio = np.where(impulso == np.amax(impulso))[0][0] - fs
				inicio = 0 if (inicio < 0) else inicio
				impulso = impulso[ :] # Corta el audio desde un segundo antes del maximo, hay que ver si esta bien esto
				impulso = (impulso/max(impulso)) * 0.8 #normalizo el audio
				sf.write(Directorio + "/RIRs/" + name + "_" + str(n)+  "_RIR"  + ".wav",impulso,fs,subtype='PCM_16') #Guarda el impulso en 16 bits
			else:
				if 'filtroinverso2' in locals():
					impulso = signal.convolve(Data[n*((silence_duration+sweep_duration)*fs2):(n*((silence_duration+sweep_duration)*fs2))+((silence_duration+sweep_duration)*fs2)],filtroinverso2,mode = 'same') / sumfil2#FFFFFF#FFFFFF  #Convoluciona el audio con el filtro inverso
					impulso = impulso[np.where(impulso == np.amax(impulso))[0][0] - fs2 :] # Corta el audio desde un segundo antes del maximo, hay que ver si esta bien esto
					impulso = (impulso/max(impulso)) * 0.8 #normalizo el audio
					sf.write(Directorio + "/RIRs/" + name + "_" + str(n)+  "_RIR" + ".wav",impulso,fs2,subtype='PCM_16') #Guarda el impulso en 16 bits
				else:
					samples = round(len(filtroinverso) * (fs2/fs))
					filtroinverso2 = signal.resample(filtroinverso,samples) #Resample a fs2
					sumfil2 = sum(filtroinverso2)
					impulso = signal.convolve(Data[n*((silence_duration+sweep_duration)*fs2):(n*((silence_duration+sweep_duration)*fs2))+((silence_duration+sweep_duration)*fs2)],filtroinverso2,mode = 'same') / sumfil2  #Convoluciona el audio con el filtro inverso
					impulso = impulso[np.where(impulso == np.amax(impulso))[0][0] - fs2 :] # Corta el audio desde un segundo antes del maximo, hay que ver si esta bien esto
					impulso = (impulso/max(impulso)) * 0.8 #normalizo el audio
					sf.write(Directorio + "/RIRs/" + name + "_" + str(n)+ "_RIR"+ ".wav",impulso,fs2,subtype='PCM_16') #Guarda el impulso en 16 bits


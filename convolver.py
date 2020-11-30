import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from scipy import signal
from tqdm import tqdm
import soundfile as sf


def convolver(inverse_directory, directory):
    try:
        os.mkdir(os.path.join(directory, "RIRs"))
    except:
        print("El directorio RIRs ya existe")
    RIR_directory = os.path.join(directory, "RIRs")
    inverse_filter, SR = sf.read(inverse_directory)
    sumfil = sum(inverse_filter)
    wav_files = [
        (os.path.join(directory, file))
        for file in os.listdir(directory)
        if (
            os.path.isfile(os.path.join(directory, file))
            and os.path.splitext(file)[1] == ".wav"
        )
    ]

    for entry in tqdm(wav_files):
        name = os.path.basename(entry)
        name = os.path.splitext(entry)[0] + "_RIR.wav"
        new_name = os.path.join(RIR_directory, name)
        Data, SR = sf.read(entry)
        if len(Data.shape) != 1:
            Data = Data[:, 0]
        RIR = signal.convolve(Data, inverse_filter, mode="same") / sumfil
        RIR = RIR[np.where(RIR == np.amax(RIR))[0][0] - SR :]
        RIR = (RIR / max(RIR)) * 0.8
        sf.write(new_name, RIR, SR, subtype="PCM_16")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    inverse_directory = filedialog.askopenfilename(title="Cargar filtro inverso")
    initial_directory = os.path.dirname(inverse_directory)

    directory = filedialog.askdirectory(
        initialdir=initial_directory,
        title="Directorio de los archivos para convolucionar",
    )
    convolver(inverse_directory, directory)
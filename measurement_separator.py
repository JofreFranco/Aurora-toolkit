import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
import soundfile as sf


def measurement_separator(
    audio, SR, sweep_length, silence_duration, RT_margin, directory
):
    N_measurements = np.int(
        len(audio) / ((int(silence_duration + int(sweep_length)) * SR))
    )
    for n in range(N_measurements):
        if n == 0:
            measurement_length = (sweep_length + silence_duration - RT_margin) * SR
        else:
            measurement_length = (sweep_length + silence_duration) * SR
        measurement_start = measurement_length * n
        measurement_end = measurement_length * (n + 1)
        measurement = audio[measurement_start:measurement_end]
        name = f"measurement_{n}.wav"
        name = os.path.join(directory, name)
        sf.write(name, measurement, SR, subtype="PCM_16")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(title="Cargar audio con las mediciones")
    audio, SR = sf.read(filename)
    directory = os.path.split(filename)[0]
    sweep_length = input("Ingresar duracion del sine sweep: ")
    silence_duration = input("Ingresar duracion del silencio después del sweep: ")
    RT_margin = input("Ingresar margen para el TR: ")
    measurement_separator(
        audio, SR, sweep_length, silence_duration, RT_margin, directory
    )

import tkinter as tk
from tkinter import filedialog
import re
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd


def AuroraText(filename="", Parameter="T30"):
    if filename == "":
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename()
    Aurorafile = pd.read_csv(filename, "\t")
    data = {"File_Name / Frequency [Hz]": list(Aurorafile["Filename"])}
    for col in Aurorafile.columns:
        col2 = col
        if col.startswith(Parameter):
            col = col.replace(Parameter + "_", "")
            if len(col.split("k", 1)) > 1:
                col = float(col.split("k", 1)[0])
                col = col * 1000
                col = str(col)
            i = 0
            for n in Aurorafile[col2]:
                if n == "--":
                    Aurorafile[col2][i] = None
                else:
                    if len(n.split(" ", 1)) > 1:
                        n = n.split(" ", -1)[-1]
                    n = n.replace(",", ".")
                    Aurorafile[col2][i] = float(n)
                i += 1
            data[col] = list(Aurorafile[col2])

    data = pd.DataFrame(data)
    mean = list(data.mean(axis=0, skipna=True))
    mean.insert(0, "Mean")
    std = list(data.std(axis=0, skipna=True))
    std.insert(0, "Standard Deviation")
    median = list(data.median(axis=0, skipna=True))
    median.insert(0, "Median")
    data.loc[len(data)] = median
    data.loc[len(data)] = mean
    data.loc[len(data)] = std
    return data


if __name__ == "__main__":
    data = AuroraText(filename="/home/francoj/AcousticParameters.txt")

import tkinter as tk
from tkinter import filedialog
import re
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import csv
from collections import OrderedDict


class Dimension_error(Exception):
    pass


class Parameter_type_error(Exception):
    pass


class Parameter(list):
    def __init__(self, parameter, frequency):
        super(Parameter, self).__init__(parameter)
        self.frequency = frequency
        self.mean = self.__calculate_mean()
        self.std = self.__calculate_std()
        self.median = self.__calculate_median()

    def plot_mean(self, show=True, save=False, deviation=True, unit=""):
        if self.name:
            name = self.name
        else:
            name = ""
        fig, ax = plt.subplots()
        ax.plot(self.frequency, self.mean)  # plotear
        ax.set(xlabel="Frequency [Hz]", ylabel=name + unit)
        plt.grid(True)
        if save:
            pass
            # codigo para guardar el plot
        if show:
            plt.show()
        else:
            return plot

    def calculate_global(self):
        global_parameter = ""  # calcular el parametro global
        return global_parameter

    def __calculate_mean(self):
        mean = []  # calcular el promedio
        for n in range(len(self[0])):
            element = [number[n] for number in self[:]]
            mean_element = np.nanmean(element)
            mean.append(mean_element)
        return mean

    def __calculate_std(self):
        std = ""  # calcular el desvio
        return std

    def __calculate_median(self):
        median = ""  # calcular la media
        return median

    def remove_outliers(self, in_place=False):
        parameter = ""  # sacar los outliers
        new_parameter_instance = Parameter(
            parameter, self.frequency
        )  # se instancia de nuevo el parametro sin los outliers para volver a calcular el promedio, etc.
        if in_place:
            self.__dict__.update(new_parameter_instance.__dict__)
        else:

            return new_parameter_instance

    def single_measure(self, n):
        if n > len(self):
            raise Dimension_error()
        return self[n]

    def add_name(self, name):
        self.name = name


class Measurement(dict):
    def __init__(self, *args, **kwds):
        super(Measurement, self).__init__(*args, **kwds)
        self.__dict__ = self
        self.__add_names()

    def print_pdf(self):
        pass

    def __add_names(self):
        for key in self.__dict__:
            self.__dict__[key].add_name(key)


def get_headers(filepath):
    with open(filepath) as auroratext:
        csv_reader = csv.reader(auroratext, delimiter="\t")
        for n_row, row in enumerate(csv_reader):
            if n_row == 2:
                header = row
                break
            else:
                pass
    header = header[1:]
    parameter_names = [column.split("_")[0] for column in header]
    parameter_names = list(OrderedDict.fromkeys(parameter_names))
    frequencies_raw = []
    for column in header:
        if column.startswith(parameter_names[0]):
            frequencies_raw.append(column.split("_")[1])
        else:
            break
    frequencies_raw = frequencies_raw[:-2]
    frequencies = []
    for number in frequencies_raw:
        try:
            frequencies.append(float(number))
        except:
            number = number.replace("k", "")
            number = float(number) * 1000
            frequencies.append(number)
    return frequencies, parameter_names

    # return frequencies


def AuroraText(frequencies, parameter_names, filepath=""):
    if filepath == "":
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()
    n_f = len(frequencies) + 2
    with open(filepath) as auroratext:
        csv_reader = csv.reader(auroratext, delimiter="\t")
        measurement_dict = {}
        for parameter in parameter_names:
            measurement_dict[parameter] = []
        for n_row, row in enumerate(csv_reader):
            row = row[1:]
            for n_element, element in enumerate(row):
                element = element.replace(" ", "")
                element = element.replace(",", ".")
                try:
                    element = float(element)
                except:
                    element = np.nan
                row[n_element] = element
            if n_row == 0 or n_row == 1 or n_row == 2:
                continue
            else:
                for n, parameter in enumerate(parameter_names):
                    start = n * n_f
                    end = ((n + 1) * n_f) - 2
                    measurement_dict[parameter].append(row[start:end])

        for parameter in parameter_names:
            measurement_dict[parameter] = Parameter(
                measurement_dict[parameter], frequencies
            )
        return Measurement(measurement_dict)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(title="Cargar archivo de aurora")
    root.destroy()

    frequencies, parameter_names = get_headers(filepath)
    asf = AuroraText(frequencies, parameter_names, filepath=filepath)
    asf.T30.plot_mean()
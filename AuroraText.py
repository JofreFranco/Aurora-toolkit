import tkinter as tk
from tkinter import filedialog
import re
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import csv
from collections import OrderedDict
import time
import warnings


class Dimension_error(Exception):
    def __init__(self, message):
        self.message = message
        print(self.message)


class Parameter_type_error(Exception):
    pass


class Parameter(list):
    def __init__(self, parameter, frequency):
        super(Parameter, self).__init__(parameter)
        self.frequency = frequency

        if not np.nansum(self):
            self.mean = np.nan
            self.std = np.nan
            self.median = np.nan
            self.global_parameter = np.nan
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.mean = self.__calculate_mean()
                self.std = self.__calculate_std()
                self.median = self.__calculate_median()
                self.global_parameter = self.__calculate_global()

    def plot_mean(
        self,
        show=True,
        save=False,
        deviation=True,
        label="",
        unit="",
        reference=False,
        **kwds,
    ):
        if self.name:
            name = self.name
        else:
            name = ""
        fig, ax = plt.subplots()
        ax.plot(self.frequency, self.mean, label=label)  # plotear
        ax.set(xlabel="Frequency [Hz]", ylabel=name + unit)
        plt.grid(True)
        if kwds:
            for key, value in kwds:
                ax.plot(value, label=key)
        if save:
            pass
            # codigo para guardar el plot
        if show:
            plt.show()
        else:
            return ax

    def __calculate_global(self):

        global_parameter = np.nanmean(self.mean)  # calcular el parametro global
        return global_parameter

    def __calculate_mean(self):
        numpy_array = np.array(self)
        n_frequencies = len(numpy_array[0][:])
        mean = []
        for n in range(n_frequencies):
            element_mean = np.nanmean(numpy_array[:, n])
            mean.append(element_mean)
        return mean

    def __calculate_std(self):
        numpy_array = np.array(self)
        n_frequencies = len(numpy_array[0][:])
        std = []
        for n in range(n_frequencies):
            element_std = np.nanstd(numpy_array[:, n])
            std.append(element_std)
        return std

    def __calculate_median(self):
        numpy_array = np.array(self)
        sum_array = np.nansum(numpy_array)

        if sum_array:
            n_frequencies = len(numpy_array[0][:])
            median = []
            for n in range(n_frequencies):
                element_median = np.nanmedian(numpy_array[:, n])
                median.append(element_median)
            return median
        else:
            return np.nan

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
        if n > len(self) - 1:
            raise Dimension_error(
                f"n should be a number between 0 and the number of measurements minus 1. {n} index is out of range"
            )
        return self[n]

    def add_name(self, name):
        self.name = name

    def add_reference(self, reference):
        self.reference = reference

    def __check_emptyness(self):
        if not np.nansum(self):
            return True
        else:
            return False


class Measurement(dict):
    def __init__(self, *args, **kwds):
        super(Measurement, self).__init__(*args, **kwds)
        self.__dict__ = self
        self.__add_names()
        self.__print_status()

    def print_pdf(self):
        pass

    def __add_names(self):
        for key in self.__dict__:
            self.__dict__[key].add_name(key)

    def __print_status(self):
        for key, value in self.items():
            if not np.nansum(value):
                print(
                    "Warning: "
                    + key
                    + " was empty, all its values and attributes will be nan. Some methods may raise errors."
                )


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
                    parameter_row = row[start:end]
                    measurement_dict[parameter].append(parameter_row)

        for parameter in parameter_names:
            nancheck = np.nansum(measurement_dict[parameter])
            if not nancheck:
                measurement_dict[parameter] = [np.nan]
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
    # asf.T30.single_measure(7)

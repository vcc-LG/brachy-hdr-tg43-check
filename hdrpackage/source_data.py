import csv
import numpy as np


def read_file(full_path):
    """
    Read in CSV files
    """
    in_file = open(full_path, "r")
    reader = csv.reader(in_file)
    input_data = []
    for row in reader:
        input_data.append(row)
    in_file.close()
    return input_data


def make_radial_dose(radial_dose_raw):
    """
    Create radial dose function from raw input data
    """
    r_cm = []
    gL = []
    for i in range(1, len(radial_dose_raw)):
        r_cm.append(float(radial_dose_raw[i][0]))
        gL.append(float(radial_dose_raw[i][1]))
    return RadialDoseClass(r_cm, gL)


class RadialDoseClass:
    """
    Class to hold radial dose function
    """

    def __init__(self, r_cm, gL):
        self.r_cm = r_cm
        self.gL = gL


def make_anisotropy_function(anisotropy_function_raw):
    """
    Create anisotropy function from raw input data
    """
    A = [[row for row in anisotropy_function_raw[i][0]]
         for i in range(2, len(anisotropy_function_raw))]
    theta = [float("".join(A[i])) for i in range(len(A))]
    B = anisotropy_function_raw[1][1:]
    r_cm = [float(i) for i in B]
    C = [[row for row in anisotropy_function_raw[i][1:]]
         for i in range(2, len(anisotropy_function_raw))]
    F = np.zeros([len(C), len(C[0])])
    for i in range(len(C)):
        for j in range(len(C[i])):
            if i != -1:
                try:
                    F[i][j] = float(C[i][j])
                except ValueError:
                    F[i][j] = None
            elif i == -1:
                F[i][j] = None
    return AnisotropyFunctionClass(r_cm, theta, F)


class AnisotropyFunctionClass:
    """
    Class to hold anisotropy function
    """

    def __init__(self, r_cm, theta, F):
        self.r_cm = r_cm
        self.theta = theta
        self.F = F


def find_nearest(array, value):
    """
    Find the index of the closest value in an array
    """
    idx = (np.abs(array - value)).argmin()
    return array[idx]

radialDose = make_radial_dose(
    read_file(r'hdrpackage\\source_files\\v2r_ESTRO_radialDose.csv'))
anisotropyFunc = make_anisotropy_function(
    read_file(r'hdrpackage\\source_files\\v2r_ESTRO_anisotropyFunction.csv'))

if __name__ == '__main__':
    print("Ran as script")
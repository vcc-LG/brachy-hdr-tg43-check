"""Perform TG43 calculations"""

from __future__ import division

from scipy.spatial.distance import pdist
from scipy import interpolate
from hdrpackage.source_data import *


def find_nearest(array, value):
    """
    Find the index of the closest value in an array
    """
    idx = (np.abs(array - value)).argmin()
    return array[idx]


class PointPosition:
    """
    Class to hold special point location
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.coords = [x, y, z]


class SourcePosition:
    """
    Class to hold source description data
    """

    def __init__(
            self,
            x,
            y,
            z,
            apparent_activity,
            dwell_time,
            Sk,
            dose_rate_constant,
            L,
            t_half):
        self.x = x
        self.y = y
        self.z = z
        self.apparent_activity = apparent_activity
        self.dwellTime = dwell_time
        self.coords = [x, y, z]
        self.Sk = Sk  # air kerma strength cGy.cm2/hr
        # dose rate constant cGy/(h.U)
        self.dose_rate_constant = dose_rate_constant
        self.L = L
        self.t_half = t_half


def get_geometry_function(my_source, my_point):
    """
    Calculate the geometry function
    x = out of plane, y = vertical, z = source axis
    """
    rRef = 1  # cm
    thetaRef = np.pi / 2  # 90 degrees
    betaRef = 2 * np.arctan((my_source.L / 2) / rRef)
    GlRef = betaRef / (my_source.L * rRef * np.sin(thetaRef))

    Gl = []
    ##################################################################
    R2 = pdist([[my_source.x, my_source.y, my_source.z], [
        my_point.x, my_point.y, my_point.z - (my_source.L / 2)]])
    R1 = pdist([[my_source.x, my_source.y, my_source.z], [
        my_point.x, my_point.y, my_point.z + (my_source.L / 2)]])
    ###################################################################
    R = pdist([[my_source.x, my_source.y, my_source.z],
               [my_point.x, my_point.y, my_point.z]])

    theta1 = np.arccos((my_point.z - my_source.z + (my_source.L / 2)) / R1)
    theta2 = np.arccos((my_point.z - my_source.z - (my_source.L / 2)) / R2)

    theta = np.arccos((my_point.z - my_source.z) / R)

    if theta == 0 or theta == np.pi:
        Gl = 1 / (R ** 2 - (my_source.L ** 2 / 4))
    else:
        beta = np.abs(theta2 - theta1)
        Gl = beta / (my_source.L * R * np.sin(theta))

    Glout = Gl / GlRef
    #    print  "Gl = %.3f, Glref = %.3f"%(Gl,GlRef)
    #    print  "thl = %.3f, th2 = %.3f"%(theta1,theta2)
    #    print  "R1 = %.3f, R2 = %.3f"%(R1,R2)
    return Glout


def nan_helper(y):
    """
    Return the indexes of NaNs in list
    """
    return np.isnan(y), lambda z: z.nonzero()[0]


def log_interp(xdata, ydata, xnew):
    """
    Perform log linear interpolation
    """
    logx = np.log(xdata)
    logy = np.log(ydata)
    return np.exp(np.interp(np.log(xnew), logx, logy))


def linear_interp_2d(xdata, ydata, zdata, xnew, ynew):
    """
    Perform linear 2D interpolation
    """
    f = interpolate.interp2d(xdata, ydata, zdata, kind='linear')
    znew = f(xnew, ynew)
    return znew


def get_radial_dose(radial_dose_in, dwell_in, point_in):
    """
    Calculate the radial dose function value
    """
    R = pdist([[dwell_in.x, dwell_in.y, dwell_in.z],
               [point_in.x, point_in.y, point_in.z]])
    if R in radial_dose_in.r_cm:
        return radial_dose_in.gL[radial_dose_in.r_cm.index(R)]
    elif R > max(radial_dose_in.r_cm) or R < min(radial_dose_in.r_cm):
        nrVal = find_nearest(np.array(radial_dose_in.r_cm), R)
        return radial_dose_in.gL[radial_dose_in.r_cm.index(nrVal)]
    else:
        return log_interp(radial_dose_in.r_cm, radial_dose_in.gL, R)


def get_anisotropy_function(anisotropy_function, my_source, my_point):
    """
    Calculate the anisotropy function value
    """
    R = pdist([[my_source.x, my_source.y, my_source.z],
               [my_point.x, my_point.y, my_point.z]])
    theta = np.degrees(np.arccos((my_point.z - my_source.z) / R))
    # print "R = %.3f, theta = %.2f"%(R,theta)
    if R in anisotropy_function.r_cm and theta in anisotropy_function.theta:
        return anisotropy_function.F[
            anisotropy_function.theta.index(theta)][
            anisotropy_function.r_cm.index(R)]
    elif R > max(anisotropy_function.r_cm) or R < min(anisotropy_function.r_cm) or theta > max(
            anisotropy_function.theta) or theta < min(anisotropy_function.theta):
        nrValR = find_nearest(np.array(anisotropy_function.r_cm), R)
        nrValtheta = find_nearest(np.array(anisotropy_function.theta), theta)
        return anisotropy_function.F[
            anisotropy_function.theta.index(nrValtheta)][
            anisotropy_function.r_cm.index(nrValR)]
    else:
        return linear_interp_2d(
            anisotropy_function.r_cm,
            anisotropy_function.theta,
            anisotropy_function.F,
            R,
            theta)


class DosePointClass:
    """
    Class to hold relevant values for dose point
    """

    def __init__(
            self,
            my_source,
            my_point,
            radial_dose_value,
            anisotropy_function_value,
            geometry_function_value,
            dose_rate_out,
            dose_total_out):
        self.my_source = my_source
        self.my_point = my_point
        self.radial_dose_value = radial_dose_value
        self.anisotropy_function_value = anisotropy_function_value
        self.geometry_function_value = geometry_function_value
        self.dose_rate_out = dose_rate_out
        self.dose_total_out = dose_total_out

    def print_values(self):
        """
        Method to print out helpful dose point descriptors
        """
        print("Source @ %s" % self.my_source.coords)
        print("Point @ %s" % self.my_point.coords)
        print("Dwell time = %.2f s" % self.my_source.dwellTime)
        print("Air kerma strength Sk = %.2f U" % self.my_source.Sk)
        print("Apparent activity Aapp = %.2f Ci" % self.my_source.Aapp)
        print("Radial dose g(r) = %.3f" % self.radial_dose_value)
        print(
            "Anisotropy function F(r,theta) = %.3f" %
            self.anisotropy_function_value)
        print(
            "Geometry function G(r,theta) = %.3f" %
            self.geometry_function_value)
        print("Dose rate = %.3f Gy/h" % self.dose_rate_out)
        print("Total dose = %.3f Gy" % self.dose_total_out)

    def print_dose(self):
        """
        Method to print out total dose
        """
        print("%.3f" % self.dose_total_out)


def calculate_my_dose(my_source, my_point, anisotropy_function, radial_dose_function):
    """
    Calculate the total dose at a point
    """
    radial_dose_val = get_radial_dose(
        radial_dose_function, my_source, my_point)
    anisotropy_func_val = get_anisotropy_function(
        anisotropy_function, my_source, my_point)
    geometry_func_val = get_geometry_function(my_source, my_point)
    dose_rate_out = my_source.Sk * my_source.dose_rate_constant * geometry_func_val * \
                    anisotropy_func_val * radial_dose_val * (1 / 100)
    dose_total_out = dose_rate_out * (my_source.dwellTime / (60 * 60))
    return DosePointClass(
        my_source,
        my_point,
        radial_dose_val,
        anisotropy_func_val,
        geometry_func_val,
        dose_rate_out,
        dose_total_out)


def make_special_points(special_points_raw):
    """
    Feed raw data into special points class
    """
    x_points = []
    y_points = []
    z_points = []
    for i in range(1, len(special_points_raw)):
        x_points.append(float(special_points_raw[i][0]))
        y_points.append(float(special_points_raw[i][1]))
        z_points.append(float(special_points_raw[i][2]))
    return SpecialPointsClass(x_points, y_points, z_points)


class SpecialPointsClass:
    """
    Create Class of special points
    """

    def __init__(self, x_points, y_points, z_points):
        self.xPoints = x_points
        self.yPoints = y_points
        self.zPoints = z_points
        self.numSpecialPoints = len(x_points)

    def print_special_points(self):
        for i in range(len(self.xPoints)):
            print("x = %.1f, y = %.1f, z = %.1f" %
                  (self.xPoints, self.yPoints, self.zPoints))


"""x = out of plane, y = vertical, z = source axis"""
"""Distances in cm"""


def make_source_trains(source_class):
    source_train = []
    for channel in source_class.channels:
        for source in channel:
            source_train.append(
                SourcePosition(
                    x=source.coords[0] / 10,  # lateral
                    y=source.coords[2] / 10,  # sup-inf
                    z=source.coords[1] / 10,  # ant-post
                    apparent_activity=10,
                    dwell_time=source.dwell_time,
                    Sk=source_class.ref_air_kerma_rate,
                    dose_rate_constant=1.108,
                    L=0.35,
                    t_half=source_class.half_life))
    return source_train


def calculate_dose(source_train_in, poi_in):
    dose = 0
    my_point = PointPosition(
        poi_in.coords[0] / 10,  # lateral
        poi_in.coords[2] / 10,  # sup-inf
        poi_in.coords[1] / 10)  # ant-post
    for dwell in source_train_in:
        my_dose = calculate_my_dose(
            dwell,
            my_point,
            anisotropyFunc,
            radialDose)
        dose += my_dose.dose_total_out
    # print("%.3f" % dose)
    return dose.tolist()[0]


if __name__ == '__main__':
    print("Ran as script")

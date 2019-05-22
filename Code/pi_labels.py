import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction

#Sourced from:
#https://github.com/MaxNoe/python-plotting/blob/master/source/create_pi_labels.py

def create_pi_labels(a=0, b=2, step=0.5, ax=None, direction='x'):
    """
    A function that gives back ticks an labels in radians
    Keyword arguments:
    a -- lower limit is a*pi (default 0.0)
    b -- upper limit is b*pi (default 2.0)
    step -- step is step*pi  (default 0.5)
    ax -- if ax is not None then ticks and labels are set for this axes (default None)
    direction -- 'x' or 'y' or 'z' (default 'x') which axis you want to label
    return value is ticks, labels
    """

    max_denominator = int(1/step)
    values = np.arange(a, b+0.1*step, step)
    fracs = [Fraction(x).limit_denominator(max_denominator) for x in values]
    ticks = values*np.pi

    if plt.rcParams["text.usetex"] is True:
        vspace = r"\vphantom{\frac{1}{2}}"
    else:
        vspace = ""

    labels = []

    for frac in fracs:
        if frac.numerator==0:
            labels.append(r"$0" + vspace + "$")
        elif frac.numerator<0:
            if frac.denominator==1 and abs(frac.numerator)==1:
                labels.append(r"$-\pi" + vspace + "$")
            elif frac.denominator==1:
                labels.append(r"$-{}\pi".format(abs(frac.numerator)) +vspace + "$")
            else:
                labels.append(r"$-\frac{{{}}}{{{}}} \pi$".format(abs(frac.numerator), frac.denominator))
        else:
            if frac.denominator==1 and frac.numerator==1:
                labels.append(r"$\pi" + vspace + "$")
            elif frac.denominator==1:
                labels.append(r"${}\pi".format(frac.numerator) + vspace + "$")
            else:
                labels.append(r"$\frac{{{}}}{{{}}} \pi$".format(frac.numerator, frac.denominator))

    if ax is not None:
        if direction == 'x':
            ax.set_xticks(ticks)
            ax.set_xticklabels(labels)
        elif direction == 'y':
            ax.set_yticks(ticks)
            ax.set_yticklabels(labels)
        elif direction == 'z':
            ax.set_zticks(ticks)
            ax.set_zticklabels(labels)
        else:
            print("direction ", direction, "is not a proper argument")

    return ticks, labels

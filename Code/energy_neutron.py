from math import *
import numpy as np
import matplotlib.pyplot as plt
from pi_labels import create_pi_labels

'''
Returns theoretical energy of emitted neutron in MeV
A - mass number of target nucleus
E_gamma - energy of gammas in MeV
Q - threshold energy in MeV for gamma-n reaction in nuclues of mass A
theta - direction between impinging gamma and direction neutron is emitted
'''

def E_n(target, E_gamma, Q = 0, theta = 0):
    #Target properties
    if target == 'beryllium':
        A = 9

        if not Q:
            Q = 1.67
    elif target == 'deuterium':
        A = 2

        if not Q:
            Q = 2.23
    else:
        print('Unknown target')
        return

    #Calculate energy
    if theta:
        return ((A - 1) / A) * (E_gamma - Q - (E_gamma**2 / (1862 * \
                (A - 1)))) + delta(A, E_gamma, Q, theta)
    else:
        return ((A - 1) / A) * (E_gamma - Q - (E_gamma**2 / (1862 * \
                (A - 1)))) + delta_max(A, E_gamma, Q, theta)

#Delta function - spread in energy
def delta(A, E_gamma, Q, theta):
    return E_gamma * np.sqrt((2 * (A - 1) * (E_gamma - Q)) / (931 * \
                              A**3)) * np.cos(theta)

#If gamma rays are isotropic
def delta_max(A, E_gamma, Q, theta):
    return 2 * E_gamma * np.sqrt((2 * (A - 1) * (E_gamma - Q)) / \
                                 (931 * A**3))

def plot(x, y, source):
    ax.plot(x, y, label = source, xunits=radians)

#Initial variables - info gathered from TOI
isotopes = ['Al-26', 'Bi-207', 'Co-58', 'Eu-150', 'Sb-124', 'Y-88', 'Bi-214']
target = ['beryllium', 'beryllium', 'beryllium', 'beryllium',
           'beryllium', 'beryllium', 'deuterium']
E_gamma = [1.808, 1.770, 1.674, 1.690, 1.69, 1.836, 2.447]
PLOT = True
TEST = False
fig = plt.figure(figsize = (12, 6), dpi = 100)
ax = fig.add_subplot(1, 1, 1)

#Test case to make sure output matches
#https://www.osti.gov/servlets/purl/4448374
if TEST:
    #Outputs 0.249 MeV which is close enough to 0.24 from paper
    #Note: they use outdated values for E_gamma and Q

    #Yttrium on Beryllium
    print(E_n('beryllium', 1.9, 1.63) * 1000)

    #Radium on Deuterium
    print(E_n('deuterium', 2.2, 2.185) * 1000)

#Print energies for given info
for i, source in enumerate(isotopes):
    print(source + ':', 'on target:', target[i], E_n(target[i], E_gamma[i]) * 1000, 'keV')

    #Plot theta distributions
    if PLOT:
        x = []
        y = []
        for e in np.arange(0.01, 2 * pi, 0.01):
            x.append(e)
            y.append(E_n(target[i], E_gamma[i], 0, e) * 1000)
        ax.plot(x, y, label = source, xunits=radians)

if PLOT:
    ax.legend(loc = 'best')
    ax.legend(bbox_to_anchor = (1, 1.02))
    ax.set_xlabel('$\\theta$')
    ax.set_ylabel('E$_n$ (keV)')
    create_pi_labels(min(x) / pi, max(x) / pi, 0.5, ax, "x")
    ax.set_title('Neutron Energy Distributions over $\\theta$')
    plt.show()

'''
Creates a plot for bubble rates at a range of threshold
energies.

Columns:
event_id vertx verty vertz atomcode blank edep blank x y z blank i blank parentid cstep initenergy
'''

import os, sys
import numpy as np
from math import *
import matplotlib.pyplot as plt
import glob
import pandas as pd
import re
from data_operations import *
from file_operations import *

def GAMMA_EFFICIENCY(x):
    '''
    Extrapolates the gamma efficiency line from
    the electron recoil paper to other energies.
    '''
    
    return np.exp(z[0] * x + z[1])

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#Data obtained from electron recoil paper
gamma_data = np.array([[1.0058411214953271, 0.007920574089622979],
[1.500584112149533, 0.00021662151984653302],
[1.9994158878504666, 0.000005459118954712787],
[2.4982476635514024, 1.4041855888046096E-7],
[3.0011682242990654, 3.6864424638037873E-9],
[3.5, 9.482206606180869E-11]])

#Fit semilog line to data
x = gamma_data[:, 0]
y = gamma_data[:, 1]
z = np.polyfit(x, np.log(y), 1)

COLUMNS = ["event_id",
           "vertx", 
           "verty",
           "vertz",
           "atomcode",
           "blank",
           "edep",
           "blank",
           "x",
           "y",
           "z",
           "blank",
           "i",
           "blank",
           "parentid",
           "cstep",
           "initenergy"]
plt.figure()

def plot_separate_multiplicities(particle_files, rate):
    '''
    Splits the data into separate bubble multiplicities
    and calculates the average bubble rates for a range
    of threshold energies.
    '''

    mults = [1, 2, 3]

    #Do this for every bubble multiplicity

    for mult in mults:
        #Initialize
        event_rates = []

        #Sort to better keep track of progress in console output
        particle_files.sort(key = natural_keys)

        thresh_range = np.arange(1, 15, 0.5)
        
        #Used for error in bubble rates, holds arrays for each particle
        n_bubbles = np.zeros(len(thresh_range))
        tot_time = 0

        #Iterate over every file and perform data analysis
        for pmt_file in particle_files:
            #Initialize
            thresh_energies = []
            bubble_rates = []

            data = open_file(pmt_file)
            
            #Select events with specific occurrence number
            if mult == 3:
                event_num = [key for key, count in Counter(data.iloc[:, 0]).items() if count >= mult]            
            else:
                event_num = [key for key, count in Counter(data.iloc[:, 0]).items() if count == mult]
            data = data[data.iloc[:, 0].isin(event_num)]

            #Remove electron recoils
            #data = data[data[4] != 11]

            #Get data
            xdata = get_column_data(data, column_id)
            
            #Iterate over every energy threshold
            for j, energy in enumerate(thresh_range):
                #Filter events below threshold
                xdata = xdata[xdata >= energy]

                #Get bubble rates
                bubble_rate, event_n_bubbles, event_time = calculate_bubble_rates(xdata, tot_events, energy, rate, True, data, True)

                #Append to arrays
                bubble_rates.append(bubble_rate)
                thresh_energies.append(energy)

                #Count number of bubbles and time for error
                n_bubbles[j] += event_n_bubbles
            tot_time += event_time

            #Store rates for each simulation
            event_rates.append(bubble_rates)

        #Statistics
        mus = np.mean(event_rates, axis = 0)
        sigmas = np.sqrt(n_bubbles / (tot_time * 100)) #scale to 100 hours

        #Display Plot
        plt.scatter(thresh_energies, mus, label = "Bubble Multiplicity {}".format(mult))
        plt.errorbar(thresh_energies, mus, sigmas, linestyle = "None", capsize = 0)

if __name__ == "__main__":
    #Grab all pmthit files in the specified directory
    if len(sys.argv) == 7:
        #Initialize arrays for files and particle types
        file_list = []
        particle_list = []

        neutron_path = sys.argv[1]

        #Check for subfolders - include subfiles if there, or only do single file
        if not neutron_path:
            pass
        elif ".out" in neutron_path:
            file_list.append([neutron_path])
            particle_list.append("Neutron")
        elif not any_subdir(neutron_path):
            file_list.append(glob.glob(neutron_path + "/*.out"))
            particle_list.append("Neutron")
        else:
            file_list.append(glob.glob(neutron_path + "/*/*.out*", recursive = True))
            particle_list.append("Neutron")

        gamma_path = sys.argv[2]

        #Check for subfolders - include subfiles if there, or only do single file
        if not gamma_path:
            pass
        elif ".out" in gamma_path:
            file_list.append([gamma_path])
            particle_list.append("Gamma")
        elif not any_subdir(gamma_path):
            file_list.append(glob.glob(gamma_path + "/*.out"))
            particle_list.append("Gamma")
        else:
            file_list.append(glob.glob(gamma_path + "/*/*.out*", recursive = True))
            particle_list.append("Gamma")

        #Simulation parameters
        column_id = int(sys.argv[3])         #see above, 6 is energy upon collision
        tot_events = int(sys.argv[4])        #num in /run/beamon
        neutron_rate = float(sys.argv[5])
        gamma_rate = float(sys.argv[6])
        min_max_energy = 1E50                #used to set y limits of plot
    else:
        print("Incorrect number of arguments, should be: neutron_dir gamma_dir col tot_events neutron_rate gamma_rate")
        sys.exit()

    #Plot separate multiplicities
    if "Neutron" in particle_list:
        index = particle_list.index("Neutron")

        plot_separate_multiplicities(file_list[index], neutron_rate)

    #Run selected files from neutron and gamma separately
    for i, particle in enumerate(particle_list):
        #Initialize
        event_rates = []

        #Grab files for specific particle
        particle_files = file_list[i]

        #Sort to better keep track of progress in console output
        particle_files.sort(key = natural_keys)

        #Set corresponding weight
        if particle == "Neutron":
            rate = neutron_rate
        elif particle == "Gamma":
            rate = gamma_rate

        #Need gammas to have high sampling range close to 1, so use different x-ranges
        if particle == "Neutron":
            thresh_range = np.arange(1, 15, 0.5)
        else:
            thresh_range = np.concatenate([np.arange(0.9, 3.5, 0.1), np.arange(3.5, 15, 0.5)])

        #Used for error in bubble rates, holds arrays for each particle
        n_bubbles = np.zeros(len(thresh_range))
        tot_time = 0

        #Iterate over every file and perform data analysis
        for pmt_file in particle_files:
            print(pmt_file)
            
            #Initialize
            ylimit = 0
            thresh_energies = []
            bubble_rates = []

            #Get data
            data = open_file(pmt_file)
            xdata = get_column_data(data, column_id)

            #Iterate over every energy threshold
            for j, energy in enumerate(thresh_range):
                #Filter events below threshold
                xdata = xdata[xdata >= energy]

                #Get bubble rates
                bubble_rate, event_n_bubbles, event_time = calculate_bubble_rates(xdata, tot_events, energy, rate, True, data)

                #Include gamma efficiency factor
                if particle == "Gamma":
                    bubble_rate *= GAMMA_EFFICIENCY(energy)

                #Append to arrays
                bubble_rates.append(bubble_rate)
                thresh_energies.append(energy)

                #Count number of bubbles and time for error
                if particle == "Gamma":
                    n_bubbles[j] += event_n_bubbles * GAMMA_EFFICIENCY(energy)
                else:
                    n_bubbles[j] += event_n_bubbles
            tot_time += event_time

            #Store rates for each simulation
            event_rates.append(bubble_rates)

        #Statistics
        mus = np.mean(event_rates, axis = 0)
        sigmas = np.sqrt(n_bubbles / (tot_time * 100)) #scale to 100 hours
        
        #Get smallest max energy for y limits
        if (np.amax(event_rates) < min_max_energy) and particle ==  "Neutron":
            min_max_energy = np.amax(event_rates)

        #Display Plot
        plt.scatter(thresh_energies, mus, label = particle)
        plt.errorbar(thresh_energies, mus, sigmas, linestyle = "None", capsize = 0)

    #Get title from filename
    title = pmt_file.split("/")[-1]
    title = title.split("_")[2]

    plt.title(title)
    plt.legend()
    plt.ylim([-0.1, min_max_energy + min_max_energy / 10])
    #plt.semilogy()
    plt.ylabel("Bubble Rate (1/hr)")
    plt.xlabel("Threshold Energy (keV)")
    plt.show()
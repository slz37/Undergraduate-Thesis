'''
Calculates the average bubble multiplicity for a range of threshold values.
Inputs are two file paths, used to plot the bubble multiplicity for 60mm
and 18mm.

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
from collections import Counter
from data_operations import *
from file_operations import *

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

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

if __name__ == "__main__":
  #Grab all pmthit files in the specified directory
  if len(sys.argv) == 3:
    path = sys.argv[1]

    #Check for subfolders - include subfiles if there, or only do single file
    if ".out" in path:
      file_list1 = [path]
    elif not any_subdir(path):
      file_list1 = glob.glob(sys.argv[1] + "/*.out")
    else:
      file_list1 = glob.glob(path + "/*/*.out*", recursive = True)

    #Check for subfolders - include subfiles if there, or only do single file
    path = sys.argv[2]

    if ".out" in path:
      file_list2 = [path]
    elif not any_subdir(path):
      file_list2 = glob.glob(sys.argv[2] + "/*.out")
    else:
      file_list2 = glob.glob(path + "/*/*.out*", recursive = True)

    files = [file_list1, file_list2]
  elif len(sys.argv) == 2:
    path = sys.argv[1]

    #Check for subfolders - include subfiles if there, or only do single file
    if ".out" in path:
      file_list1 = [path]
    elif not any_subdir(path):
      file_list1 = glob.glob(sys.argv[1] + "/*.out")
    else:
      file_list1 = glob.glob(path + "/*/*.out*", recursive = True)

    files = [file_list1]
  else:
    print("Incorrect number of arguments.")
    sys.exit()

  thresh_range = np.arange(1, 15, 0.5)
  colors = ["tab:purple", "g"]

  for i, file_list in enumerate(files):
    #Initialize
    bubble_multiplicity = []
    sigmas = []

    #Sort to better keep track of progress in console output
    file_list.sort(key = natural_keys)

    #Run through all files
    for pmt_file in file_list:
        print(pmt_file)

        #Load data
        data = open_file(pmt_file)

        #Array for averages at each threshold
        avgs = []

        #Loop over all threshold energies and get bubble multiplicity
        for energy in thresh_range:
            #Cut data to only greater than threshohld
            data = data[data.iloc[:, 6] * 1000 >= energy] 
            xdata = get_column_data(data, 0)

            _, event_n_bubbles, time = calculate_bubble_rates(xdata, 1000000, energy, 0.3, True, data)

            #Get average
            multiplicity = list(Counter(xdata).values())
            avg = np.mean(multiplicity)
            sigmas.append(sqrt(event_n_bubbles * 100 / time) / (len(multiplicity) * 100 / time))

            #Add to array for file averages
            avgs.append(avg)
        
        #Now add to total array for all simulations
        bubble_multiplicity.append(avgs)

    #Get mean
    mus = np.mean(bubble_multiplicity, axis = 0)
    #sigmas = np.std(bubble_multiplicity, axis = 0)

    #Plot
    plt.scatter(thresh_range, mus, color = colors[i])
    plt.errorbar(thresh_range, mus, sigmas, color = colors[i], linestyle = "None", capsize = 0)

  plt.xlabel("Threshold Energy (keV)")
  plt.ylabel("Average bubble multiplicity")
  plt.semilogy()
  plt.legend(["PICO-40L", "PICO-500"], loc = "best")
  plt.show()
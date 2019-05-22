'''
Takes in all pmt files in a directory, plots a histogram of the 
recoil energies for carbon and fluorine.

Columns:
event_id vertx verty vertz atomcode blank edep blank x y z blank i blank parentid cstep initenergy
'''

import os, sys
import numpy as np
from math import *
import matplotlib.pyplot as plt
import glob
from astropy.visualization import hist as fancyhist
import pandas as pd
import re
from data_operations import *
from file_operations import *

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
plt.figure()#figsize = (20, 10))

def get_bins(trimmed_xdata):
    '''
    Returns the bins for histograms
    '''
    tot_events = len(trimmed_xdata)
    #Bins for trimmed data
    q25 = np.percentile(trimmed_xdata, 25)
    q75 = np.percentile(trimmed_xdata, 75)
    SigmaG = astroMLstats.sigmaG(trimmed_xdata)
    binsize = 2.7 * SigmaG / (tot_events**(1. / 3))
    bins = np.append(np.arange(start = 0.2,#trimmed_xdata.min(), 
                    stop = max(trimmed_xdata), step = binsize), max(trimmed_xdata))
    #bins = np.append(0., bins)

    return bins

if __name__ == "__main__":
  #Grab all pmthit files in the specified directory
  if len(sys.argv) == 6:
    path = sys.argv[1]

    #Check for subfolders - include subfiles if there, or only do single file
    if ".out" in path:
      file_list = [path]
    elif not any_subdir(path):
      file_list = glob.glob(sys.argv[1] + "/*.out")
    else:
      file_list = glob.glob(path + "/*/*.out*", recursive = True)

    column_id = int(sys.argv[2])

    #Simulation parmeters
    tot_events = int(sys.argv[3]) #total num events
    thresh = int(sys.argv[4]) #bubble nucleation threshold
    rate = float(sys.argv[5]) #source rate
  else:
    print("Incorrect number of arguments, should be: dir col #events bubble_thresh source_rate.")
    sys.exit()

  #Initialize arrays
  carbon_data = []
  fluorine_data = []
  
  #Iterate over every file and perform data analysis
  for pmt_file in file_list:
    #Load and scale energies to keV
    data = open_file(pmt_file)
    data.iloc[:, 6] *= 1000
    
    #Get fluorine recoils
    fdata = data.loc[data.iloc[:, 4] == 9019]
    
    #fdata =  fdata.loc[fdata.iloc[:, 6] > 0]
    
    fdata = fdata.iloc[:, 6].values
    fluorine_data.append(fdata)

    #Get carbon recoils
    cdata = data.loc[data.iloc[:, 4] == 6000]

    #cdata =  cdata.loc[cdata.iloc[:, 6] > 0]

    cdata = cdata.iloc[:, 6].values
    carbon_data.append(cdata)

  #Flatten arrays
  carbon_data = [item for sublist in carbon_data for item in sublist]
  fluorine_data = [item for sublist in fluorine_data for item in sublist]

  #Get bins
  fbins = get_bins(fluorine_data)
  cbins = get_bins(carbon_data)

  #Plot the data from the neutrino recoil plot
  v_data = pd.read_csv("/home/salvatore/Documents/pico_simulations/pico-svn/DBC-from-40/build/recoil_data.txt", delim_whitespace = True)
  v_x = v_data.iloc[:, 0]
  v_f = v_data.iloc[:, 1]
  v_c = v_data.iloc[:, 2]
  plt.plot(v_x, v_c, label = "$\\nu$-C", color = "mediumslateblue")
  plt.plot(v_x, v_f, label = "$\\nu$-F", color = "darkolivegreen")

  #Display Plot
  plt.hist(x = carbon_data, weights = np.ones_like(carbon_data)*7.60443/100000, bins = cbins, density = False, histtype = "step", label = "n-C", color = "tab:purple")
  plt.hist(x = fluorine_data, weights = np.ones_like(fluorine_data)*7.60443/100000, bins = fbins, density = False, histtype = "step", label = "n-F", color = "g")
  plt.semilogy()
  plt.semilogx()
  plt.grid(True, which = "major", axis = "both", ls = "-")
  plt.grid(True, which = "minor", axis = "both", ls = ":")
  plt.legend(loc = "best")
  plt.xlabel("Recoil Energy (keV)")
  plt.ylabel("Events")
  plt.show()

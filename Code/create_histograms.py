'''
Takes in all pmt files in a directory and overplots the histograms
for the specified columns.

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
plt.figure(figsize = (20, 10))

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
  
  ylimit = 0

  #Iterate over every file and perform data analysis
  for pmt_file in file_list:
    data = open_file(pmt_file)

    xdata = get_column_data(data, column_id)

    n = create_histogram(pmt_file, xdata, tot_events, thresh, rate)

    #Set ylimits to be max of the trimmed xdata
    if max(n[1:]) > ylimit:
      ylimit = max(n[1:])

  #Get string to save figure as
  filename_convention = r"(?<=C3F8_)[\w]+(?=.)"
  file_label = re.search(filename_convention, pmt_file).group()

  #Display Plot
  plt.axvline(x = thresh, color = "r")
  plt.text(thresh + 0.5, ylimit + (ylimit / 20), "Bubble Nucleation Threshold", color = "r")
  plt.legend()
  plt.ylim([0, ylimit + ylimit / 10])
  plt.xlabel(COLUMNS[column_id])
  plt.savefig("histogram_{}".format(file_label))
  plt.show()

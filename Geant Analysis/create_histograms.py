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
plt.figure(figsize = (20, 10), dpi = 75)

if __name__ == "__main__":
  #Grab all pmthit files in the specified directory
  if len(sys.argv) == 3:
    path = sys.argv[1]

    #Check for subfolders - include subfiles if there
    if any_subdir(path):
      file_list = glob.glob(sys.argv[1] + "/*.out*")
    else:
      file_list = glob.glob(path + "/*/*.out*", recursive = True)

    column_id = int(sys.argv[2])  
  else:
    print("Incorrect number of arguments.")
    sys.exit()

  tot_events = 100000

  #Iterate over every file and perform data analysis
  for pmt_file in file_list:
    data = open_file(pmt_file)

    xdata = get_column_data(data, column_id)

    create_histogram(pmt_file, xdata, tot_events)

  #Get string to save figure as
  filename_convention = r"(?<=C3F8_)[\w]+(?=.)"
  file_label = re.search(filename_convention, pmt_file).group()

  #Display Plot
  plt.legend()
  plt.xlabel(COLUMNS[column_id])
  plt.savefig("histogram_{}".format(file_label))
  plt.show()

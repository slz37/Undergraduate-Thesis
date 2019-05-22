'''
Makes a histogram of the energy distrbution of a source
from read_output.sh
'''

import os, sys
import numpy as np
from math import *
import matplotlib.pyplot as plt
import glob
from astropy.visualization import hist as fancyhist
import pandas as pd
import re
from file_operations import *

COLUMNS = ["event_id",
           "energy"]
plt.figure()#figsize = (20, 10))

def open_file(filename):
  '''
  Takes in a filename, opens it, and returns
  the data contained within it.
  '''

  #Load data separated by non-uniform white space and no headers
  data = pd.read_csv(filename, header = None, delim_whitespace = True)

  return data

def get_column_data(data, column_id):
  '''
  Takes in hit data loaded from .out files and
  returns an array containing the data of the
  specified column.
  '''

  #Grab column data
  xdata = data.iloc[:, column_id].values[:]

  return xdata

if __name__ == "__main__":
  #Grab all pmthit files in the specified directory
  if len(sys.argv) == 2:
    path = sys.argv[1]
    filel = glob.glob(sys.argv[1] + "/initial_data.txt")
  else:
    print("Incorrect number of arguments.")
    sys.exit()

  data = open_file(filel[0])
  xdata = get_column_data(data, 1)
  fancyhist(xdata, bins = "scott", density = True, histtype = "step", label = "Cm244")

  #Display Plot
  plt.legend()
  plt.xlabel("E$_{n}$(MeV)")
  plt.savefig("energy_spectrum.png")
  plt.show()

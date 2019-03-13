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

  #Scale energy to keV
  if column_id == 6:
    xdata *= 1000

  return xdata

def get_statistics(xdata):
  '''
  Takes in x-data for a histogram and computes relevant
  statistical parameters.
  '''
  total = len(xdata)
  mean = np.mean(xdata)  

  return total, mean

def create_histogram(filename, xdata):
  '''
  Takes in the column data from a .out hit file
  and sets the histogram properties of it.
  '''
  
  #Filename convention: particle_C3F8_LABEL
  #Look behind for C3F8_ and ahead for . but don't include
  filename_convention = r"(?<=C3F8_)[\w]+(?=.)"
  file_label = re.search(filename_convention, filename).group()

  #Add statistics to label
  total, mean = get_statistics(xdata)
  file_label += "\nNum_hits: " + str(total) + "\nMean: " + str(mean) + "\n"

  fancyhist(xdata, bins = "scott", density = False, histtype = "step", label = file_label)

if __name__ == "__main__":
  #Grab all pmthit files in the specified directory
  if len(sys.argv) == 3:
    #file_list = glob.glob(sys.argv[1] + "/*.out*")
    file_list = glob.glob(sys.argv[1] + "/*/*.out*", recursive = True)
    column_id = int(sys.argv[2])  
  else:
    print("Incorrect number of arguments.")
    sys.exit()
  print(sys.argv[1] + "*/*.out*")
  #Iterate over every file and create histogram
  for pmt_file in file_list:
    data = open_file(pmt_file)

    xdata = get_column_data(data, column_id)

    create_histogram(pmt_file, xdata)

  #Get string to save figure as
  filename_convention = r"(?<=C3F8_)[\w]+(?=_)"
  file_label = re.search(filename_convention, pmt_file).group()

  #Display Plot
  plt.legend()
  plt.xlabel(COLUMNS[column_id])
  plt.savefig("histogramtot_{}".format(file_label))
  plt.show()

'''
Functions for performing all necessary file operations to read data from GEANT4.

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

def any_subdir(path):
  '''
  Returns a boolean value if the current directory
  contains any subdirectories
  '''

  #Loop through items and return true if one is a directory
  for filename in os.walk(path):
    if os.path.isdir(os.path.join(path)):
      return True

  return False

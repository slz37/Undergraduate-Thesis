'''
Contains the data analysis functions used with the main program to analyze data output from GEANT4.

Columns:
event_id vertx verty vertz atomcode blank edep blank x y z blank i blank parentid cstep initenergy
'''

import os, sys
import numpy as np
from math import *
import matplotlib.pyplot as plt
import glob
from astropy.visualization import hist as fancyhist
from astroML import stats as astroMLstats
import pandas as pd
import re
from file_operations import get_column_data
from collections import Counter

PER_SEC_TO_PER_HR = 3600

def get_bubble_multiplicity(data):
  '''
  Calculates the average bubble multiplicity
  to normalize the threshold count to events
  and not total bubbles.
  '''

  #Grab event number and count number of bubbles for each event
  xdata = get_column_data(data, 0)
  bubble_multiplicity = list(Counter(xdata).values())

  #Calculate statistics
  avg = np.mean(bubble_multiplicity)

  return avg

def calculate_bubble_rates(xdata, tot_events, THRESH, RATE, errors = False, data = [], norm = True):
  '''
  Takes in the data loaded from the .out files
  and calculates the rate bubbles form per hour
  based on the neutron emission rate, number of
  events, and events that were above the threshold.
  '''

  if norm:
    #Get bubble multiplicity to scale by event rather than total bubbles
    threshold_data = data[data.iloc[:, 6] >= THRESH] 
    
    #If nothing above threshold, then scaling factor doesn't matter anyway
    if threshold_data.empty:
      threshold_multiplicity_avg = 1
    else:
      threshold_multiplicity_avg = get_bubble_multiplicity(threshold_data)

    threshold_count = sum(xdata >= THRESH) / threshold_multiplicity_avg
    time = (tot_events / RATE) / PER_SEC_TO_PER_HR

    bubble_rate = threshold_count / time

    #Return data for calculating errors if requested
    if errors:
      return bubble_rate, threshold_count, time

    return bubble_rate
  else:
    threshold_count = sum(xdata >= THRESH)
    time = (tot_events / RATE) / PER_SEC_TO_PER_HR

    bubble_rate = threshold_count / time

    #Return data for calculating errors if requested
    if errors:
      return bubble_rate, threshold_count, time

    return bubble_rate

def trim_threshold(xdata, THRESH):
  '''
  Takes in data from GEANT4 and removes all points
  below the threshold energy for bubble nucleation.
  This clears up histograms a bunch.
  '''

  mask = (xdata > THRESH)
  new_xdata = xdata[mask]

  return new_xdata

def get_statistics(xdata, THRESH, data = []):
  '''
  Takes in x-data for a histogram and computes relevant
  statistical parameters.
  '''

  #Get bubble multiplicity to scale by event rather than total bubbles
  bubble_multiplicity_avg = get_bubble_multiplicity(data)

  total = len(xdata) / bubble_multiplicity_avg

  #Get multiplicity for events greater than threshold
  threshold_data = data[data.iloc[:, 6] >= THRESH] 
  threshold_multiplicity_avg = get_bubble_multiplicity(threshold_data)

  mean = np.mean(xdata) / threshold_multiplicity_avg
  threshold_count = sum(xdata >= THRESH) / threshold_multiplicity_avg

  return total, mean, threshold_count

def create_histogram(filename, xdata, tot_events, THRESH, RATE, data = []):
  '''
  Takes in the column data from a .out hit file
  and sets the histogram properties of it.
  '''
  
  #Filename convention: particle_C3F8_LABEL
  #Look behind for C3F8_ and ahead for . but don't include
  filename_convention = r"(?<=C3F8_)[\w]+(?=.)"
  file_label = re.search(filename_convention, filename).group()

  #Add statistics to label
  total, mean, threshold_count = get_statistics(xdata, THRESH, data)
  bubble_rate = calculate_bubble_rates(xdata, tot_events, THRESH, RATE, False, data)
  #file_label += #"\nNum_hits: " + str(int(round(total))) + \
                #"\nMean (keV): " + str(round(mean, 2)) + \
                #"\nHits above threshold: " + str(int(round(threshold_count))) + \
  file_label += "\nBubble rate (n/Hr): " + str(round(bubble_rate, 2))

  #Now that calulations are done, cut to threshold energy
  trimmed_xdata = trim_threshold(xdata, THRESH)

  #Bins for trimmed data
  q25 = np.percentile(trimmed_xdata, 25)
  q75 = np.percentile(trimmed_xdata, 75)
  SigmaG = astroMLstats.sigmaG(trimmed_xdata)
  binsize = 2.7 * SigmaG / (tot_events**(1. / 3))
  bins = np.append(np.arange(start = THRESH,#trimmed_xdata.min(), 
                    stop = trimmed_xdata.max(), step = binsize), trimmed_xdata.max())
  bins = np.append(0., bins)

  n, _, _ = plt.hist(x = xdata, bins = bins, density = False, histtype = "step", label = file_label)
  #fancyhist(xdata, bins = "scott", density = False, histtype = "step", label = file_label)

  return n

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:31:45 2019

@author: ZHANG Mofan
"""

# Main

import numpy as np
import cfg as cfg
from pydef import *
import datetime
print("#####################################################")
print("Street network and inputs data batch preprocessing...")
print("This script can be used to prepare data for MUNICH.")
print("Author: ZHANG Mofan")
print("EDF R&D - CEREA joint laboratory with ENPC")
print("Programming language: Python 3.7")
print("Time of preprocessing: " + str(datetime.datetime.now()))
print("#####################################################")
# -------------------------------------------------------------------
# .dat
# Creat new street segments and intersections
print("Street network preprocessing phase:")
print("#####################################################")
len_min = cfg.len_min
true_inter_indicator = cfg.true_inter_indicator
file_street = cfg.file_street
file_intersection = cfg.file_intersection
file_street_new = cfg.file_street_new
file_intersection_new = cfg.file_intersection_new
print("-----------------------------------------------------")
print("Reading .dat files...")
parameters_street, parameters_inter = read_inputs_dat(file_street,
                                                      file_intersection)
print("Completed.")
print("-----------------------------------------------------")
print("Street network preprocessing...")
parameters_street_new, parameters_inter_new = streetnetworkpreprocessing(parameters_street,
                                                                         parameters_inter, len_min)
print("Completed.")
print("-----------------------------------------------------")
print("Writing .dat files...")
write_outputs_dat(parameters_street_new,
                  parameters_inter_new,
                  file_street_new,
                  file_intersection_new,
                  true_inter_indicator)
print("Completed.")
print("-----------------------------------------------------")
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# .bin
print("#####################################################")
print("Inputs preprocessing phase:")
print("#####################################################")
treat_emission = cfg.treat_emission
treat_background = cfg.treat_background
treat_meteo = cfg.treat_meteo
treat_photolysis = cfg.treat_photolysis
shape_street = cfg.shape_street
shape_inter = cfg.shape_inter
bindir = cfg.bindir
inputspreprocessing(bindir,
                    parameters_street,
                    parameters_street_new,
                    parameters_inter_new,
                    shape_street,
                    shape_inter,
                    treat_emission,
                    treat_background,
                    treat_meteo,
                    treat_photolysis)
# -------------------------------------------------------------------

print("#####################################################")
print('All new data files are noted by a "_new" suffix.')
print("#####################################################")
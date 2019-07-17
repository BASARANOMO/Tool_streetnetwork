#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:14:50 2019

@author: ZHANG Mofan
"""

# Configuration file

# -------------------------------------------------------------------
# .dat
# Length minimum of road segments to be devided
len_min = 50    # m

# Are we going to mark down whether an intersection is created artificially or not?
# yes == 1, no == 0
true_inter_indicator = 0

file_street = '/home/f05079/Documents/Polyphemus/Test/Inputs/street.dat'
file_intersection = '/home/f05079/Documents/Polyphemus/Test/Inputs/intersection.dat'
file_street_new = '/home/f05079/Documents/Polyphemus/Test/Inputs/street_new.dat'
file_intersection_new = '/home/f05079/Documents/Polyphemus/Test/Inputs/intersection_new.dat'
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# .bin, meteo and others
# meteo, background, emission, photolysis
shape_street = [2568, 577] # Nt x Nstreet
shape_inter = [2568, 433] # Nt x Ninter
bindir = '/home/f05079/Documents/Polyphemus/Test/Inputs/'
treat_emission = 1
treat_background = 1
treat_meteo = 1
treat_photolysis = 0
# -------------------------------------------------------------------
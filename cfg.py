#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:14:50 2019

@author: ZHANG Mofan
"""

# Configuration file for StreetNetworkPreprocessing.py

# Length minimum of road segments to be devided
len_min = 50    # m

# Are we going to mark down whether an intersection is created artificially or not?
# yes == 1, no == 0
true_inter_indicator = 0

file_street = 'street.dat'
file_intersection = 'intersection.dat'
file_street_new = 'street_new.dat'
file_intersection_new = 'intersection_new.dat'
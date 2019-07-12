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

len_min = cfg.len_min
true_inter_indicator = cfg.true_inter_indicator
file_street = cfg.file_street
file_intersection = cfg.file_intersection
file_street_new = cfg.file_street_new
file_intersection_new = cfg.file_intersection_new

parameters_street, parameters_inter = read_inputs_dat(file_street, file_intersection)
parameters_street_new, parameters_inter_new = streetnetworkpreprocessing(parameters_street, parameters_inter, len_min)
write_outputs_dat(parameters_street_new, parameters_inter_new, file_street_new, file_intersection_new, true_inter_indicator)
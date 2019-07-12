#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:07:06 2019

@author: ZHANG Mofan
"""

def meteopreprocessing(data, street_corr):
    data_new = data.copy()
    
    n_street = 0
    for i in range(len(street_corr)):
        n_street += len(street_corr[i]) # count new raod segments
        
    for i in range(data.shape[1]):
        for j in range(len(street_corr[i]) - 1):
            data_new = np.insert(data_new, 1, data_LMO[:, 1], axis = 1)
    return data_new

def read_meteo(file_name, shape):
    length = 1
    for l in shape:
        length *= l
    data = np.fromfile(file_name, 'f', length)
    data.shape = shape
    data = data.astype('d')
    return data
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:07:06 2019

@author: ZHANG Mofan
"""
import numpy as np

def meteopreprocessing_street(data_street_old, street_corr):
    data_new = data_street_old.copy() 
    n_street_added = 0
    for i in range(data_street_old.shape[1]):
        for j in range(len(street_corr[i]) - 1):
            data_new = np.insert(data_new, i + 1 + n_street_added, data_street_old[:, i], axis = 1)
            n_street_added += 1
    return data_new

def meteopreprocessing_inter(data_inter_old, data_street_old, inter_corr):
    data_new = data_inter_old.copy()
    for i in range(len(inter_corr)):
        if ~np.isnan(inter_corr[i]):
            #print(data_street_old[:, inter_corr[i], None].shape)
            data_new = np.append(data_new, data_street_old[:, inter_corr[i], None], axis = 1)
    return data_new

def read_meteo(file_name, shape):
    length = 1
    for l in shape:
        length *= l
    data = np.fromfile(file_name, 'f', length)
    data.shape = shape
    data = data.astype('d')
    return data

def write_meteo(file_name, data):
    data_flatten = data.flatten().astype('f')
    with open(file_name, 'wb') as f_write_meteo:
        for i in range(len(data_flatten)):
            f_write_meteo.write(data_flatten[i])
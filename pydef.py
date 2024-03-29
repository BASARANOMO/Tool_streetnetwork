#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 13:24:25 2019

@author: ZHANG Mofan
"""
# Functional programming

import numpy as np
import glob, os
from shutil import copyfile

def read_inputs_dat(file_street = 'street.dat', 
                    file_intersection = 'intersection.dat'):
    # Initialization
    # street.dat
    street_id = []
    begin_inter = []
    end_inter = []
    length = []
    width = []
    height = []

    # intersection.dat
    inter_id = []
    x_inter = []
    y_inter = []
    nstreet = []
    street_list = []
    
    # street.dat
    with open(file_street, 'r') as f1:
        d1 = f1.readlines()
        for i in d1:
            k1 = i.rstrip().split(";")
            street_id.append(int(k1[0]))
            begin_inter.append(int(k1[1]))
            end_inter.append(int(k1[2]))
            length.append(float(k1[3]))
            width.append(float(k1[4]))
            height.append(float(k1[5]))

    # intersection.dat
    with open(file_intersection, 'r') as f2:
        d2 = f2.readlines()
        n_line = 0
        for i in d2:
            k2 = i.rstrip().split(";")
            inter_id.append(int(k2[0]))
            x_inter.append(float(k2[1]))
            y_inter.append(float(k2[2]))
            nstreet.append(int(k2[3]))
            street_list.append([])
        
            for j in range(nstreet[n_line]):
                street_list[n_line].append(int(k2[4 + j]))
            n_line = n_line + 1
                
    parameters_street = {"street_id": street_id,
                         "begin_inter": begin_inter,
                         "end_inter": end_inter,
                         "length": length,
                         "width": width,
                         "height": height}
    parameters_inter = {"inter_id": inter_id,
                        "x_inter": x_inter,
                        "y_inter": y_inter,
                        "nstreet": nstreet,
                        "street_list": street_list}
    
    return parameters_street, parameters_inter

def streetnetworkpreprocessing(parameters_street, parameters_inter, len_min):
    # Initialization
    street_id = parameters_street["street_id"]
    begin_inter = parameters_street["begin_inter"]
    end_inter = parameters_street["end_inter"]
    length = parameters_street["length"]
    width = parameters_street["width"]
    height = parameters_street["height"]
    inter_id = parameters_inter["inter_id"]
    x_inter = parameters_inter["x_inter"]
    y_inter = parameters_inter["y_inter"]
    nstreet = parameters_inter["nstreet"]
    street_list = parameters_inter["street_list"]
    
    # street_new and intersection_new
    street_id_new = []
    begin_inter_new = []
    end_inter_new = []
    length_new = []
    width_new = []
    height_new = []
    street_corr = []
    inter_id_new = inter_id.copy()
    x_inter_new = x_inter.copy()
    y_inter_new = y_inter.copy()
    nstreet_new = nstreet.copy()
    street_list_new = street_list.copy()
    true_inter = [1] * len(inter_id) 
    inter_corr = [np.nan] * len(inter_id) 
    # This parameter is used to distinguish true intersections and virtual intersections
    
    # Create new road segments and intersections
    inter_id_max = np.max(inter_id)
    street_id_max = np.max(street_id)
    count_street_new = 1 # count number of new streets
    count_inter_new = 1 # count number of new intersections
    for i in range(len(street_id)):
        md = length[i] // len_min # number of new segments
        for j in range(len(inter_id)):
            if begin_inter[i] == inter_id[j]:
                x_b = x_inter[j]
                y_b = y_inter[j]
            if end_inter[i] == inter_id[j]:
                x_e = x_inter[j]
                y_e = y_inter[j]
        if md == 0:
            street_id_new.append(count_street_new)
            begin_inter_new.append(begin_inter[i])
            end_inter_new.append(end_inter[i])
            length_new.append(length[i])
            width_new.append(width[i])
            height_new.append(height[i])
            street_corr.append([count_street_new])
            count_street_new += 1
        
            # Adapt street_list
            for k in range(len(inter_id)):
                if inter_id[k] == begin_inter[i]:
                    for l in range(len(street_list[k])):
                        if street_list[k][l] == street_id[i]:
                            street_list_new[k][l] = count_street_new - 1
                if inter_id[k] == end_inter[i]:
                    for l in range(len(street_list[k])):
                        if street_list[k][l] == street_id[i]:
                            street_list_new[k][l] = count_street_new - 1
                        
        elif md >= 1:
            delta_x = (x_e - x_b) / (md + 1)
            delta_y = (y_e - y_b) / (md + 1)
            delta_length = length[i] / (md + 1)
            # Create new intersections
            for k in range(int(md)):
                inter_id_new.append(count_inter_new + inter_id_max)
                x_inter_new.append(x_b + (k + 1) * delta_x)
                y_inter_new.append(y_b + (k + 1) * delta_y)
                nstreet_new.append(2)
                true_inter.append(0)
                inter_corr.append(i)
                count_inter_new += 1
            street_corr_prime = []
            # Divide this street to md new street segments
            for k in range(int(md + 1)):
                street_id_new.append(count_street_new)
                if k == 0:
                    begin_inter_new.append(begin_inter[i])
                    end_inter_new.append(inter_id_new[int(len(inter_id) + count_inter_new - md - 1)])
                elif k == md:
                    begin_inter_new.append(inter_id_new[int(len(inter_id) + count_inter_new - 2)])
                    end_inter_new.append(end_inter[i])
                else:
                    begin_inter_new.append(inter_id_new[int(len(inter_id) + count_inter_new - md + k - 2)])
                    end_inter_new.append(inter_id_new[int(len(inter_id) + count_inter_new  - md + k - 1)])
                length_new.append(delta_length)
                width_new.append(width[i])
                height_new.append(height[i])
                street_corr_prime.append(count_street_new)
                count_street_new += 1
            street_corr.append(street_corr_prime)
        
            # Adapt street_list of old intersections
            for k in range(len(inter_id)):
                if inter_id[k] == begin_inter[i]:
                    for l in range(len(street_list[k])):
                        if street_list[k][l] == street_id[i]:
                            street_list_new[k][l] = street_id_new[int(count_street_new - md - 2)]
                if inter_id[k] == end_inter[i]:
                    for l in range(len(street_list[k])):
                        if street_list[k][l] == street_id[i]:
                            street_list_new[k][l] = street_id_new[int(count_street_new - 2)]
                    
            # Adapt street_list of new intersections
            for k in range(int(md)):
                street_list_new.append([street_id_new[int(count_street_new - md + k - 2)], 
                                        street_id_new[int(count_street_new - md + k - 1)]])
    
    parameters_street_new = {"street_id_new": street_id_new,
                             "begin_inter_new": begin_inter_new,
                             "end_inter_new": end_inter_new,
                             "length_new": length_new,
                             "width_new": width_new,
                             "height_new": height_new,
                             "street_corr": street_corr}
    
    parameters_inter_new = {"inter_id_new": inter_id_new,
                            "x_inter_new": x_inter_new,
                            "y_inter_new": y_inter_new,
                            "nstreet_new": nstreet_new,
                            "street_list_new": street_list_new,
                            "true_inter": true_inter,
                            "inter_corr": inter_corr}
    
    return parameters_street_new, parameters_inter_new

def write_outputs_dat(parameters_street_new, 
                      parameters_inter_new, 
                      file_street_new = 'street_new.dat', 
                      file_intersection_new = 'intersection_new.dat', 
                      true_inter_indicator = 1):
    street_id_new = parameters_street_new["street_id_new"]
    begin_inter_new = parameters_street_new["begin_inter_new"]
    end_inter_new = parameters_street_new["end_inter_new"]
    length_new = parameters_street_new["length_new"]
    width_new = parameters_street_new["width_new"]
    height_new = parameters_street_new["height_new"]
    inter_id_new = parameters_inter_new["inter_id_new"]
    x_inter_new = parameters_inter_new["x_inter_new"]
    y_inter_new = parameters_inter_new["y_inter_new"]
    nstreet_new = parameters_inter_new["nstreet_new"]
    street_list_new = parameters_inter_new["street_list_new"]
    true_inter = parameters_inter_new["true_inter"]
    # Generate _new files
    with open(file_street_new, 'w') as f3:
        for i in range(len(street_id_new)): 
            f3.write(str(street_id_new[i]) + ';')
            f3.write(str(begin_inter_new[i]) + ';')
            f3.write(str(end_inter_new[i]) + ';')
            f3.write(str(length_new[i]) + ';')
            f3.write(str(width_new[i]) + ';')
            f3.write(str(height_new[i]))
            f3.write('\n')

    with open(file_intersection_new, 'w') as f4:
        for i in range(len(inter_id_new)): 
            f4.write(str(inter_id_new[i]) + ';')
            f4.write(str(x_inter_new[i]) + ';')
            f4.write(str(y_inter_new[i]) + ';')
            f4.write(str(nstreet_new[i]) + ';')
            for j in range(len(street_list_new[i])):
                f4.write(str(street_list_new[i][j]) + ';')
            if true_inter_indicator == 1:
                f4.write(str(true_inter[i]) + ';')
            f4.write('\n')
            
def binpreprocessing_street(data_street_old, street_corr):
    data_new = data_street_old.copy() 
    n_street_added = 0
    for i in range(data_street_old.shape[1]):
        for j in range(len(street_corr[i]) - 1):
            data_new = np.insert(data_new, i + 1 + n_street_added, data_street_old[:, i], axis = 1)
            n_street_added += 1
    return data_new

def binpreprocessing_inter(data_inter_old, data_street_old, inter_corr):
    data_new = data_inter_old.copy()
    for i in range(len(inter_corr)):
        if ~np.isnan(inter_corr[i]):
            #print(data_street_old[:, inter_corr[i], None].shape)
            data_new = np.append(data_new, data_street_old[:, inter_corr[i], None], axis = 1)
    return data_new

def emissionpreprocessing_street(data, parameters_street_old, parameters_street_new):
    data_new = np.zeros((data.shape[0], len(parameters_street_new["street_id_new"])))
    k = 0
    for i in range(data.shape[1]):
        for j in range(len(parameters_street_new["street_corr"][i])):
            data_new[:, k] = data[:, i] / parameters_street_old["length"][i] * parameters_street_new["length_new"][j]
            k += 1
    return data_new

def read_bin(file_name, shape):
    length = 1
    for l in shape:
        length *= l
    data = np.fromfile(file_name, 'f', length)
    data.shape = shape
    data = data.astype('d')
    return data

def write_bin(file_name, data):
    data_flatten = data.flatten().astype('f')
    with open(file_name, 'wb') as f_write_meteo:
        for i in range(len(data_flatten)):
            f_write_meteo.write(data_flatten[i])
            
def find_all_bin(bindir):
    file_name_list = []
    os.chdir(bindir)
    for file in glob.glob("*.bin"):
        file_name_list.append(file)
    return file_name_list

def find_all_folders(totaldir):
    folder_name_list = []
    for folder_name in os.walk(totaldir):
        folder_name_list.append(str(folder_name[0]) + "/")
    return folder_name_list

def inputspreprocessing(bindir,
                        newbindir,
                        parameters_street,
                        parameters_street_new,
                        parameters_inter_new,
                        shape_street,
                        shape_inter,
                        treat_emission =  0,
                        treat_background = 0,
                        treat_meteo = 0,
                        treat_photolysis = 0):
    data_emission = {}
    data_background = {}
    data_meteo = {}
    data_photolysis = {}
    data_emission_new = {}
    data_background_new = {}
    data_meteo_new = {}
    data_photolysis_new = {}
    folder_name_list = find_all_folders(bindir)
    for i in folder_name_list:
        file_name_list = find_all_bin(i)
        if "emission" in i and treat_emission:
            print("-----------------------------------------------------")
            print("Emission preprocessing...")
            for j in file_name_list:
                print("File name: " + j)
                data_emission[i + j] = read_bin(j, shape_street)
                data_emission_new[i + j] = emissionpreprocessing_street(data_emission[i + j], parameters_street, parameters_street_new)
                address_string = i + j
                write_bin(newbindir + 'emission/' + j, data_emission_new[i + j])
                #write_bin(address_string[:address_string.index('.')] + '_new' + address_string[address_string.index('.'):], data_emission_new[i + j])
            print("Emission preprocessing completed.")
        if "background" in i and treat_background:
            print("-----------------------------------------------------")
            print("Background preprocessing...")
            for j in file_name_list:
                print("File name: " + j)
                data_background[i + j] = read_bin(j, shape_street)
                data_background_new[i + j] = binpreprocessing_street(data_background[i + j], parameters_street_new["street_corr"])
                address_string = i + j
                write_bin(newbindir + 'background/' + j, data_background_new[i + j])
                #write_bin(address_string[:address_string.index('.')] + '_new' + address_string[address_string.index('.'):], data_background_new[i + j])
            print("Background preprocessing completed.")
        if "meteo" in i and treat_meteo:
            print("-----------------------------------------------------")
            print("Meteo preprocessing...")
            for j in file_name_list:
                print("File name: " + j)
                if "Inter" in j:
                    data_meteo[i + j] = read_bin(j, shape_inter)
                else:
                    data_meteo[i + j] = read_bin(j, shape_street)
            for j in file_name_list:
                if "Inter" in j:
                    #data_meteo[i + j] = read_bin(j, shape_inter)
                    string_inter = i + j
                    string_street = string_inter.replace('Inter.bin', '.bin')
                    data_meteo_new[i + j] = binpreprocessing_inter(data_meteo[i + j], data_meteo[string_street], parameters_inter_new["inter_corr"])
                else:
                    #data_meteo[i + j] = read_bin(j, shape_street)
                    data_meteo_new[i + j] = binpreprocessing_street(data_meteo[i + j], parameters_street_new["street_corr"])
                address_string = i + j
                write_bin(newbindir + 'meteo/' + j, data_meteo_new[i + j])
                #write_bin(address_string[:address_string.index('.')] + '_new' + address_string[address_string.index('.'):], data_meteo_new[i + j])
            print("Meteo preprocessing completed.")
        if "photolysis" in i and treat_photolysis:
            print("-----------------------------------------------------")
            print("Photolysis preprocessing...")
            for j in file_name_list:
                print("Copy file name: " + j)
                copyfile(j, newbindir + 'photolysis/' + j)
#            for j in file_name_list:
#                print("File name: " + j)
#                data_photolysis[i + j] = read_bin(j, shape_street)
#                data_photolysis_new[i + j] = binpreprocessing_street(data_photolysis[i + j], parameters_street_new["street_corr"])
            print("Photolysis preprocessing completed.")
    print("-----------------------------------------------------")
    return      


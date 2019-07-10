#! python3
"""
Created on Monday July 8th 10:31:02 2019

@author: ZHANG Mofan
"""

import numpy as np
import cfg as cfg

#--------------------------------------------------------------------------
# Read hyper parameters in cfg
# len_min: the length minimum of roads to be devided
# true_inter_indicator: we mark down whether or not an intersection is created artificially
len_min = cfg.len_min
true_inter_indicator = cfg.true_inter_indicator
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
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
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# Read inputs
# street.dat
with open('street.dat', 'r') as f1:
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
with open('intersection.dat', 'r') as f2:
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
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# Initialization
# street_new and intersection_new
street_id_new = []
begin_inter_new = []
end_inter_new = []
length_new = []
width_new = []
height_new = []
inter_id_new = inter_id.copy()
x_inter_new = x_inter.copy()
y_inter_new = y_inter.copy()
nstreet_new = nstreet.copy()
street_list_new = street_list.copy()
true_inter = [1] * len(inter_id) # This parameter is used to distinguish true intersections and virtual intersections
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
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
            
    if md == 0 or md == 1:
        street_id_new.append(count_street_new)
        begin_inter_new.append(begin_inter[i])
        end_inter_new.append(end_inter[i])
        length_new.append(length[i])
        width_new.append(width[i])
        height_new.append(height[i])
        count_street_new += 1
        
        # Adapt street_list
        for k in range(len(inter_id)):
            if inter_id[k] == begin_inter[i]:
                for l in range(len(street_list[k])):
                    if street_list[k][l] == street_id[i]:
                        street_list_new[k][l] = street_id_new[int(count_street_new - 2)]
            if inter_id[k] == end_inter[i]:
                for l in range(len(street_list[k])):
                    if street_list[k][l] == street_id[i]:
                        street_list_new[k][l] = street_id_new[int(count_street_new - 2)]
                        
    if md >= 2:
        delta_x = (x_e - x_b) / md
        delta_y = (y_e - y_b) / md
        delta_length = length[i] / md
        # Create new intersections
        for k in range(int(md - 1)):
            inter_id_new.append(count_inter_new + inter_id_max)
            x_inter_new.append(x_b + (k + 1) * delta_x)
            y_inter_new.append(y_b + (k + 1) * delta_y)
            nstreet_new.append(2)
            true_inter.append(0)
            count_inter_new += 1
        
        # Divide this street to md new street segments
        for k in range(int(md)):
            street_id_new.append(count_street_new)
            if k == 0:
                begin_inter_new.append(begin_inter[i])
                end_inter_new.append(inter_id_new[int(count_inter_new - md + k)])
            if k == md - 1:
                begin_inter_new.append(inter_id_new[int(count_inter_new - md + k - 1)])
                end_inter_new.append(end_inter[i])
            else:
                begin_inter_new.append(inter_id_new[int(count_inter_new - md + k - 1)])
                end_inter_new.append(inter_id_new[int(count_inter_new  - md + k)])
            length_new.append(delta_length)
            width_new.append(width[i])
            height_new.append(height[i])
            count_street_new += 1
        
        # Adapt street_list of old intersections
        for k in range(len(inter_id)):
            if inter_id[k] == begin_inter[i]:
                for l in range(len(street_list[k])):
                    if street_list[k][l] == street_id[i]:
                        street_list_new[k][l] = street_id_new[int(count_street_new - md - 1)]
            if inter_id[k] == end_inter[i]:
                for l in range(len(street_list[k])):
                    if street_list[k][l] == street_id[i]:
                        street_list_new[k][l] = street_id_new[int(count_street_new - 2)]
                    
        # Adapt street_list of new intersections
        for k in range(int(md - 1)):
            street_list_new.append([street_id_new[int(count_street_new - md + k - 1)], 
                                    street_id_new[int(count_street_new - md + k)]])
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# Generate _new files
with open('street_new.dat', 'w') as f3:
    for i in range(len(street_id_new)): 
        f3.write(str(street_id_new[i]) + ';')
        f3.write(str(begin_inter_new[i]) + ';')
        f3.write(str(end_inter_new[i]) + ';')
        f3.write(str(width_new[i]) + ';')
        f3.write(str(height_new[i]))
        f3.write('\n')

with open('intersection_new.dat', 'w') as f4:
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
#--------------------------------------------------------------------------            
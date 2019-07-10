Copyright: ZHANG Mofan, CEREA EDF R&D - ENPC
July 10 2019

Tool used for deviding street segments and improving spatial resolution

-------------------------------------------------------------
Inputs: street.dat and intersection.dat

In street.dat
#street_id #begin_inter #end_inter #length #width #height
In intersection.dat
#inter_id #x_inter #y_inter #nstreet #street_list
-------------------------------------------------------------

-------------------------------------------------------------
Outputs: street_new.dat and intersection_new.dat

In street_new.dat
#street_id #begin_inter #end_inter #length #width #height
In intersection_new.dat
#inter_id #x_inter #y_inter #nstreet #street_list #true_inter
-------------------------------------------------------------

#true_inter is a parameter added to distinguish true intersections and virtual intersections
true_inter = 1: intersections are just from old intersection.dat
true_inter = 0: new intersections created by the script to improve spatial resolution who have no physical senses

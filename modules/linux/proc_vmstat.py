#This module pars linux /proc/meminfo format file.
#A in this file we only need from first collumn and second we will use 
#tow_collumns funtion from modules/two_collumns.py and function pars_t1
from modules.parser import pars_t1

def pars(data, typeval):
    print (data)
    data_ = pars_t1(data, typeval)
    return data_
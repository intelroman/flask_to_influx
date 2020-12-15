#This module pars linux /proc/meminfo format file.
#A in this file we only need from first collumn and second we will use 
#tow_collumns funtion from modules/two_collumns.py and function pars_t1
# MemTotal:       16402164 kB
# MemFree:        12791288 kB
# .... 
# HugePages_Total:       0
# HugePages_Free:        0
# HugePages_Rsvd:        0
from modules.parser import pars_t1

def pars(data, typeval):
    data_ = pars_t1(data, typeval)
    return data_
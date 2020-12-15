#This module will pars uptime format.
from modules.parser import pars_t2

def pars(data, typeval):
    data_ = pars_t2(data, typeval)
    return data_
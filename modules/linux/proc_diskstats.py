#This module pars linux /proc/diskstats format file.
#https://www.kernel.org/doc/Documentation/ABI/testing/procfs-diskstats

from modules.parser import pars_custom

def pars (data, typeval, tagcols, valcols):
    data_ = pars_custom(data, typeval, tagcols, valcols)
    return data_
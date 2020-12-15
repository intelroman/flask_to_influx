'''
This function will pars 2 collumns format
example:
data: value
or
data value
It will atomaticaly remove multiple spaces and remove : or starting line with space
'''
import re
def pars_t1(data, typeval):
    retdata = {typeval: {}}
    for i in data.split("\n"):
        i = re.sub(" +", " ", i)
        i = re.sub("(:|^ +|\r)", "", i)
        n = i.split(" ")[0]
        v = i.split(" ")[1]
        retdata[typeval].update({n: v})
    return retdata

'''
This function will pars 1 lie of values
examples:
value1 value2 value3 value4
'''
def pars_t2(data, typeval):
    retdata = {}
    data = re.sub(" +", " ", data)
    data = re.sub("(:|^ +|\r)", "", data)
    for idx,i in enumerate(data.split(" ")):
        retdata.update({typeval+"_"+str(idx): {"value": i}})
    return retdata

def pars_custom(data, typeval, tagcols, valcols):
    retdata = {typeval: []}
    for idx, i in enumerate(data.split("\n")):
        i = re.sub(" +", " ", i)
        i = re.sub(":|^ +|\r|\t", "", i)
        tags = {}
        vals = {}
        index = {}
        for x in tagcols:
            tags.update({"tag_"+str(x): i.split(" ")[int(x)]})
        for x in valcols:
            vals.update({"vals_"+str(x): i.split(" ")[int(x)]})
        index.update({"tags": tags})
        index.update({"vals": vals})
        retdata[typeval].append(index)
    return retdata




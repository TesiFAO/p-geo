# http://pysal.readthedocs.org/en/v1.7/library/index.html
from pysal.esda import mapclassify as mapclassify
import numpy as np

def get_classiciation(map, type, k):
    # get all values

    # switch
    quantile()

def quantile(values, k):
    # apply quantiles
    return mapclassify.quantile(values, k)



x = np.arange(10)

print mapclassify.quantile(x)
print mapclassify.quantile(x, k = 4)
print mapclassify.quantile(x, k = 3)

cal = mapclassify.load_example()
# print mapclassify.Box_Plot(cal)

ei = mapclassify.Equal_Interval(x, k = 5)
print ei
print "counts:", ei.counts
print "bins:", ei.bins

ei = mapclassify.Natural_Breaks(x, k = 5)
print ei



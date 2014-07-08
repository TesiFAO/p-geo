# http://pysal.readthedocs.org/en/v1.7/library/index.html
from pysal.esda import mapclassify as mapclassify
import numpy as np
import brewer2mpl #https://github.com/jiffyclub/brewer2mpl



# COLORS
def colors(color, values=5, type='sequential'):
    # print brewer2mpl.print_maps()
    # print brewer2mpl.print_maps('sequential')

    # bmap = brewer2mpl.get_map('YlGn', 'sequential', 8).hex_colors
    return  brewer2mpl.get_map(color, type, values).hex_colors


print colors('YlGn', 3)


def get_classiciation(obj):
    # values, type, k, nodata=True
    # get all values (key, values)

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



import numpy as np
from osgeo import gdal

def stats(file, band):
    ds = gdal.Open(file)
    return np.array(ds.GetRasterBand(band).ReadAsArray())

print "start"
array1 = stats("/home/vortex/Desktop/LAYERS/MODIS/001/AB_NDVI_4326.tif", 1)
print "1"
array2 = stats("/home/vortex/Desktop/LAYERS/MODIS/017/AB_NDVI_4326.tif", 1)
print "2"
# array3 = stats("/home/vortex/Desktop/LAYERS/MODIS/033/AB_NDVI_4326.tif", 1)
# print "3"

# array4 = stats("/home/vortex/programs/SERVERS/tomcat_geoservers/data/data/modis/test_bella_guide3/test_bella_guide3.geotiff", 1)
# print "4"
# array5 = stats("/home/vortex/programs/SERVERS/tomcat_geoservers/data/data/modis/test_bella_guide3/test_bella_guide3.geotiff", 1)
# print "5"

print np.corrcoef(array1.ravel(), array2.ravel())
# print np.corrcoef(array1.ravel(), array3.ravel())
# print np.corrcoef(array2.ravel(), array3.ravel())
# print np.corrcoef(array4.ravel(), array5.ravel())
print "end"
import geoserver
from osgeo import ogr

import os.path
import psycopg2
import osgeo.ogr
import config
import psycopg2
import os.path
from sys import argv
import subprocess
import util
import osr
from urllib import urlencode
from urllib2 import urlopen
import json

g = geoserver.Geoserver()
#g.create_coveragestore('testasd', '/home/vortex/Desktop/TMP/output3_4326_tt_nodata.tif', 'fenix')
a = g.publish_coveragestore('test3', '/home/vortex/Desktop/LAYERS/MODIS/AB_NDVI_4326.tif', 'test')
# a = g.set_default_style('test2', 'guido_test')

#print str(a)
#g.reload_configuration_geoserver_slaves()

#g.set_default_style('evi', 'guido_test')

#g.publish_shapefile('/home/vortex/programs/layers/vector/GAUL0/g2008_0.shp', 'g2008_4326',)


#print 'END'

# g.publish_shapefile('/home/vortex/programs/layers/vector/nga_gaul1/NGA_GAUL_1.shp', 'nga_gaul1',)
#
#
# '''
# name = "aassa"
# g.delete_coveragestore(name)
# layers = {'tif': '/home/vortex/programs/layers/raster/TRMM/3B42RT/2014/touload/aa.tif', 'tfw': '/home/vortex/programs/layers/raster/TRMM/3B42RT/2014/touload/aa.tfw'}
# a = g.publish_coveragestore(name, layers )
# '''
#
#
#
#
# '''
# srs = osr.SpatialReference()
# srs.ImportFromEPSG('Mercator_Auxiliary_Sphere')
# print srs
# srs.AutoIdentifyEPSG()   ;'''

# WFS REQUEST
#http://localhost:9091/geoserver/wfs?request=describeFeatureType&outputFormat=application/json&typename=fenix:g2008_4326

